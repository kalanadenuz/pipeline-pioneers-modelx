"""Inductive Conformal Prediction (ICP) Engine."""
import numpy as np
from typing import Tuple, Dict, Any

class ConformalHydrologicalCalibrator:
    def __init__(self, alpha: float = 0.10):
        self.alpha = alpha
        self.q_val = 0.12
        self.calibrated = False

    def calibrate(self, y_calib_true: np.ndarray, y_calib_pred: np.ndarray):
        residuals = np.abs(y_calib_true - y_calib_pred)
        n = len(residuals)
        q_level = min(0.999, float(np.ceil((n + 1) * (1.0 - self.alpha + 0.05)) / n))
        self.q_val = float(np.quantile(residuals, q_level))
        self.calibrated = True
        return self.q_val

    def predict_interval(self, y_pred: np.ndarray, uncertainty_expansion: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        margin = self.q_val * uncertainty_expansion
        return np.maximum(0.0, y_pred - margin), y_pred + margin

    def evaluate_coverage(self, y_true: np.ndarray, y_low: np.ndarray, y_high: np.ndarray) -> Dict[str, Any]:
        in_bounds = (y_true >= y_low) & (y_true <= y_high)
        coverage_rate = float(np.mean(in_bounds))
        mean_interval_width = float(np.mean(y_high - y_low))
        return {
            "target_coverage": 1.0 - self.alpha,
            "empirical_coverage": coverage_rate,
            "mean_interval_width_m": mean_interval_width,
            "calibration_passed": bool(coverage_rate >= (1.0 - self.alpha - 0.02)),
        }
