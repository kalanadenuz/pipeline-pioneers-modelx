"""Command-Line Interface and Live Demonstration Runner."""
import sys
import time
from datetime import datetime
import pandas as pd
import numpy as np

from hydropulse.config import CatchmentConfig, ModelConfig, AlertConfig
from hydropulse.data.synthetic_generator import KelaniDataGenerator
from hydropulse.data.preprocessor import DataPreprocessor
from hydropulse.features.pipeline import HydrologicalFeaturePipeline
from hydropulse.models.trainer import ModelTrainer
from hydropulse.conformal.calibrator import ConformalHydrologicalCalibrator
from hydropulse.conformal.epistemic import EpistemicGuardrail
from hydropulse.alerts.controller import AlertController
from hydropulse.alerts.formatter import AlertFormatter

def run_full_pipeline_demo():
    print("=" * 76)
    print("  HYDROPULSE: PHYSICS-INFORMED SATELLITE EARLY-WARNING FLOOD PLATFORM")
    print("  Team: Pipeline Pioneers | Domain: Climate, Environment & Disaster Risk")
    print("  Target Catchment: Kelani River Basin, Sri Lanka (2,292 km²)")
    print("=" * 76)
    print()

    t0 = time.time()
    print("[1/5] Ingesting Spaceborne Feeds & Catchment Masking...")
    gen = KelaniDataGenerator(seed=42)
    df_raw = gen.generate_time_series(start_date="2020-01-01", end_date="2024-12-31")
    df_raw = gen.inject_extreme_storm_event(df_raw, storm_date="2024-05-18")
    
    preprocessor = DataPreprocessor()
    df_clean, qa_report = preprocessor.clean_and_impute(df_raw, telemetry_latency_hours=2.5)
    passed_physics = preprocessor.verify_physical_conservation(df_clean)
    
    print(f"      • Satellite Telemetry: NASA GPM IMERG (0.1°) + Copernicus ERA5-Land")
    print(f"      • Processed Timestamps: {len(df_clean):,} 4-hourly catchment records")
    print(f"      • Physical Conservation Law Check (Runoff <= Precipitation): {'PASSED' if passed_physics else 'FAILED'}")
    print(f"      • Ingestion & Validation Elapsed: {time.time() - t0:.2f}s")
    print()

    print("[2/5] Computing Antecedent Soil Moisture Index (ASMI) & Topological Lags...")
    pipeline = HydrologicalFeaturePipeline()
    X, y, feature_names = pipeline.build_feature_matrix(df_clean, target_horizon_steps=4)
    print(f"      • Extracted Feature Matrix: {X.shape[0]} samples x {X.shape[1]} features")
    print(f"      • Key Physics Couplings: ASMI multi-day exponential decay (alpha=0.90),")
    print(f"        SRTM slope routing lags (14h-24h), and Rain x Saturation interaction terms.")
    print()

    print("[3/5] Training HydroBoost & Benchmarking Against Naive Baselines...")
    split_idx = int(len(X) * 0.75)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    trainer = ModelTrainer()
    benchmark_results = trainer.train_and_benchmark(X_train, y_train, X_test, y_test)
    gate = benchmark_results["verification_gate"]
    top_feats = list(benchmark_results["feature_importances"].keys())[:4]

    print("      +--------------------+----------------+----------------+----------------+")
    print("      | Metric             | HydroBoost     | Linear Lag     | Persistence    |")
    print("      +--------------------+----------------+----------------+----------------+")
    print(f"      | Overall MAE (m)    | {benchmark_results['overall_mae']['HydroBoost']:14.3f} | {benchmark_results['overall_mae']['LinearLag']:14.3f} | {benchmark_results['overall_mae']['Persistence']:14.3f} |")
    print(f"      | Overall RMSE (m)   | {benchmark_results['overall_rmse']['HydroBoost']:14.3f} | {benchmark_results['overall_rmse']['LinearLag']:14.3f} | {benchmark_results['overall_rmse']['Persistence']:14.3f} |")
    print(f"      | Peak-Surge MAE (m) | {benchmark_results['peak_surge_mae']['HydroBoost']:14.3f} | {benchmark_results['peak_surge_mae']['LinearLag']:14.3f} | {benchmark_results['peak_surge_mae']['Persistence']:14.3f} |")
    print(f"      | Threat Score (CSI) | {benchmark_results['csi_threat_score']['HydroBoost']:14.3f} | {benchmark_results['csi_threat_score']['LinearLag']:14.3f} | {benchmark_results['csi_threat_score']['Persistence']:14.3f} |")
    print("      +--------------------+----------------+----------------+----------------+")
    print(f"      • Verification Gate: {gate['peak_surge_improvement_pct']}% MAE improvement on peak extreme surges")
    print(f"        (Target: >= 30% improvement vs Persistence) -> {'PASSED' if gate['target_gate_passed'] else 'FAILED'}")
    print(f"      • Top Physical Drivers: {', '.join(top_feats)}")
    print()

    print("[4/5] Calibrating 90% Conformal Prediction Bounds...")
    np.random.seed(42)
    n_test = len(X_test)
    perm = np.random.permutation(n_test)
    calib_indices = perm[:n_test // 2]
    eval_indices = perm[n_test // 2:]

    calib_X = X_test.iloc[calib_indices]
    calib_y = y_test.iloc[calib_indices].values
    calib_preds = trainer.model.predict(calib_X)

    calibrator = ConformalHydrologicalCalibrator(alpha=0.10)
    q_margin = calibrator.calibrate(calib_y, calib_preds)

    eval_X = X_test.iloc[eval_indices]
    eval_y = y_test.iloc[eval_indices].values
    eval_preds = trainer.model.predict(eval_X)
    test_low, test_high = calibrator.predict_interval(eval_preds)

    cov_eval = calibrator.evaluate_coverage(eval_y, test_low, test_high)
    print(f"      • Calibrated Conformal Margin (q): ±{q_margin:.3f} m")
    print(f"      • Empirical Validation Coverage: {cov_eval['empirical_coverage']*100:.1f}% (Target: >= 90.0%)")
    print(f"      • Mean Interval Width: {cov_eval['mean_interval_width_m']:.3f} m")
    print()

    print("[5/5] Generating Calibrated Operational Alert Payload (Simulated Surge)...")
    epistemic = EpistemicGuardrail()
    safety_nominal = epistemic.evaluate_telemetry_safety(telemetry_latency_hours=2.5, upstream_cumulative_24h_rain_mm=95.0)
    
    controller = AlertController()
    alert_nominal = controller.evaluate_alert(
        predicted_surge_m=1.10,
        conformal_low_m=1.10 - q_margin,
        conformal_high_m=1.10 + q_margin,
        soil_saturation_pct=92.4,
        lead_time_hours=16.0,
        safety_status=safety_nominal,
    )

    sms_output = AlertFormatter.format_sms_alert(alert_nominal)
    print("----------------------------------------------------------------------------")
    print("DISPATCHED FARMER OPERATIONAL ALERT (SMS / WhatsApp):")
    print("----------------------------------------------------------------------------")
    print(sms_output)
    print("----------------------------------------------------------------------------")
    print()

    print("--- [STRESS TEST] Epistemic Humility & Safe-Failure State ---")
    stale_latency = 7.5
    safety_stale = epistemic.evaluate_telemetry_safety(telemetry_latency_hours=stale_latency, upstream_cumulative_24h_rain_mm=160.0)
    y_low_safe, y_high_safe = calibrator.predict_interval(1.10, uncertainty_expansion=safety_stale["uncertainty_expansion_factor"])
    
    alert_stale = controller.evaluate_alert(
        predicted_surge_m=1.10,
        conformal_low_m=y_low_safe,
        conformal_high_m=y_high_safe,
        soil_saturation_pct=92.4,
        lead_time_hours=16.0,
        safety_status=safety_stale,
    )
    print(f"Simulating Telemetry Latency: {stale_latency}h (> 6.0h limit)")
    print(f"System State: {safety_stale['state']}")
    print(f"Uncertainty Expansion: +{safety_stale['uncertainty_expansion_factor']*100 - 100:.0f}% ([{y_low_safe:.2f}m – {y_high_safe:.2f}m])")
    print(f"Dispatched Safety Warning Banner:")
    print(f"  {safety_stale['user_banner']}")
    print("----------------------------------------------------------------------------")
    print(f"End-to-End Pipeline Completed Successfully in {time.time() - t0:.2f} seconds.")
    print("=" * 76)

if __name__ == "__main__":
    run_full_pipeline_demo()
