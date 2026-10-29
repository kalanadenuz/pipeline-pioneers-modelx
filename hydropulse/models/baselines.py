"""Hydrological Baseline Models."""
import numpy as np
import pandas as pd

class PersistenceBaseline:
    def fit(self, X: pd.DataFrame, y: pd.Series):
        pass

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if "current_surge_m" in X.columns:
            return np.maximum(0.0, X["current_surge_m"].values)
        elif "current_hanwella_stage" in X.columns:
            return np.maximum(0.0, X["current_hanwella_stage"].values - 1.80)
        return np.zeros(len(X))

class LinearLagBaseline:
    def __init__(self):
        self.weights = None
        self.bias = 0.0
        self.feature_cols = []

    def fit(self, X: pd.DataFrame, y: pd.Series):
        rain_cols = [c for c in X.columns if "rain" in c and "saturation" not in c and "asmi" not in c]
        if not rain_cols:
            rain_cols = list(X.columns)[:4]
        X_mat = X[rain_cols].values
        y_vec = y.values
        X_design = np.column_stack([np.ones(len(X_mat)), X_mat])
        ridge = 1e-2 * np.eye(X_design.shape[1])
        coeffs = np.linalg.solve(X_design.T @ X_design + ridge, X_design.T @ y_vec)
        self.bias = coeffs[0]
        self.weights = coeffs[1:]
        self.feature_cols = rain_cols

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        X_mat = X[self.feature_cols].values
        return np.maximum(0.0, self.bias + X_mat @ self.weights)
