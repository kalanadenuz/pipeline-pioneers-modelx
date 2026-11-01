"""Model Training, Validation, and Benchmarking."""
import numpy as np
import pandas as pd
from typing import Dict, Any
from hydropulse.models.regressor import HydroBoostRegressor
from hydropulse.models.baselines import PersistenceBaseline, LinearLagBaseline

class ModelTrainer:
    def __init__(self):
        self.model = HydroBoostRegressor(n_estimators=25, learning_rate=0.18, max_depth=4)
        self.persistence = PersistenceBaseline()
        self.linear_lag = LinearLagBaseline()

    def train_and_benchmark(self, X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame, y_test: pd.Series, surge_threshold_m: float = 0.50) -> Dict[str, Any]:
        self.model.fit(X_train, y_train)
        self.persistence.fit(X_train, y_train)
        self.linear_lag.fit(X_train, y_train)

        preds_model = self.model.predict(X_test)
        preds_pers = self.persistence.predict(X_test)
        preds_linear = self.linear_lag.predict(X_test)
        y_true = y_test.values

        peak_mask = y_true >= np.percentile(y_true, 95)
        results = {
            "overall_mae": {
                "HydroBoost": float(np.mean(np.abs(y_true - preds_model))),
                "LinearLag": float(np.mean(np.abs(y_true - preds_linear))),
                "Persistence": float(np.mean(np.abs(y_true - preds_pers))),
            },
            "overall_rmse": {
                "HydroBoost": float(np.sqrt(np.mean((y_true - preds_model) ** 2))),
                "LinearLag": float(np.sqrt(np.mean((y_true - preds_linear) ** 2))),
                "Persistence": float(np.sqrt(np.mean((y_true - preds_pers) ** 2))),
            },
            "peak_surge_mae": {
                "HydroBoost": float(np.mean(np.abs(y_true[peak_mask] - preds_model[peak_mask]))),
                "LinearLag": float(np.mean(np.abs(y_true[peak_mask] - preds_linear[peak_mask]))),
                "Persistence": float(np.mean(np.abs(y_true[peak_mask] - preds_pers[peak_mask]))),
            },
            "csi_threat_score": {
                "HydroBoost": self._calculate_csi(y_true, preds_model, threshold=surge_threshold_m),
                "LinearLag": self._calculate_csi(y_true, preds_linear, threshold=surge_threshold_m),
                "Persistence": self._calculate_csi(y_true, preds_pers, threshold=surge_threshold_m),
            },
        }

        pers_peak_mae = results["peak_surge_mae"]["Persistence"]
        model_peak_mae = results["peak_surge_mae"]["HydroBoost"]
        improvement_pct = ((pers_peak_mae - model_peak_mae) / (pers_peak_mae + 1e-6)) * 100.0
        results["verification_gate"] = {
            "peak_surge_improvement_pct": float(np.round(improvement_pct, 1)),
            "outperforms_persistence_by_30pct": bool(improvement_pct >= 30.0),
            "target_gate_passed": bool(improvement_pct >= 30.0),
        }
        importances = dict(zip(self.model.feature_names_, [float(f) for f in self.model.feature_importances_]))
        results["feature_importances"] = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))
        return results

    def _calculate_csi(self, y_true: np.ndarray, y_pred: np.ndarray, threshold: float = 0.50) -> float:
        hits = np.sum((y_pred >= threshold) & (y_true >= threshold))
        misses = np.sum((y_pred < threshold) & (y_true >= threshold))
        false_alarms = np.sum((y_pred >= threshold) & (y_true < threshold))
        denom = hits + misses + false_alarms
        return float(hits / denom) if denom > 0 else 0.0
