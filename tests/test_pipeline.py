"""Unit Tests for HydroPulse."""
import unittest
import numpy as np
import pandas as pd
from hydropulse.data.synthetic_generator import KelaniDataGenerator
from hydropulse.data.preprocessor import DataPreprocessor
from hydropulse.features.pipeline import HydrologicalFeaturePipeline
from hydropulse.models.trainer import ModelTrainer
from hydropulse.conformal.calibrator import ConformalHydrologicalCalibrator
from hydropulse.conformal.epistemic import EpistemicGuardrail

class TestHydroPulse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        gen = KelaniDataGenerator(seed=42)
        cls.df = gen.generate_time_series(start_date="2021-01-01", end_date="2024-12-31")
        cls.df = gen.inject_extreme_storm_event(cls.df, storm_date="2024-05-18")
        preprocessor = DataPreprocessor()
        cls.df_clean, _ = preprocessor.clean_and_impute(cls.df, telemetry_latency_hours=2.0)
        pipeline = HydrologicalFeaturePipeline()
        cls.X, cls.y, _ = pipeline.build_feature_matrix(cls.df_clean, target_horizon_steps=4)

    def test_physical_conservation_law(self):
        preprocessor = DataPreprocessor()
        passed = preprocessor.verify_physical_conservation(self.df_clean)
        self.assertTrue(passed)

    def test_asmi_correlation_with_monsoon(self):
        asmi = self.df_clean["asmi_mm"]
        wet_asmi = asmi[self.df_clean["timestamp"].dt.month.isin([5, 6])].mean()
        dry_asmi = asmi[self.df_clean["timestamp"].dt.month.isin([1, 2])].mean()
        self.assertGreater(wet_asmi, dry_asmi)

    def test_model_beats_persistence_by_30pct(self):
        split = int(len(self.X) * 0.70)
        X_train, X_test = self.X.iloc[:split], self.X.iloc[split:]
        y_train, y_test = self.y.iloc[:split], self.y.iloc[split:]
        trainer = ModelTrainer()
        results = trainer.train_and_benchmark(X_train, y_train, X_test, y_test)
        gate = results["verification_gate"]
        self.assertTrue(gate["outperforms_persistence_by_30pct"])

    def test_conformal_coverage_rate(self):
        split = int(len(self.X) * 0.70)
        X_train, X_test = self.X.iloc[:split], self.X.iloc[split:]
        y_train, y_test = self.y.iloc[:split], self.y.iloc[split:]
        trainer = ModelTrainer()
        trainer.model.fit(X_train, y_train)

        np.random.seed(42)
        n_test = len(X_test)
        perm = np.random.permutation(n_test)
        calib_indices = perm[:n_test // 2]
        eval_indices = perm[n_test // 2:]

        calib_X = X_test.iloc[calib_indices]
        calib_y = y_test.iloc[calib_indices].values
        calib_preds = trainer.model.predict(calib_X)

        calibrator = ConformalHydrologicalCalibrator(alpha=0.10)
        calibrator.calibrate(calib_y, calib_preds)

        eval_X = X_test.iloc[eval_indices]
        eval_y = y_test.iloc[eval_indices].values
        eval_preds = trainer.model.predict(eval_X)
        y_low, y_high = calibrator.predict_interval(eval_preds)

        cov = calibrator.evaluate_coverage(eval_y, y_low, y_high)
        self.assertGreaterEqual(cov["empirical_coverage"], 0.88)

    def test_epistemic_humility_latency_trigger(self):
        epistemic = EpistemicGuardrail()
        status_fresh = epistemic.evaluate_telemetry_safety(2.5, 50.0)
        self.assertEqual(status_fresh["state"], "OPERATIONAL_NOMINAL")
        self.assertFalse(status_fresh["telemetry_compromised"])

        status_stale = epistemic.evaluate_telemetry_safety(7.5, 50.0)
        self.assertEqual(status_stale["state"], "SAFE_FAILURE_STATE")
        self.assertTrue(status_stale["telemetry_compromised"])
        self.assertGreater(status_stale["uncertainty_expansion_factor"], 1.2)

if __name__ == "__main__":
    unittest.main()
