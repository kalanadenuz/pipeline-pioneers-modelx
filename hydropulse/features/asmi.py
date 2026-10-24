"""Antecedent Soil Moisture Index (ASMI) Computation Engine."""
import numpy as np
import pandas as pd

class ASMICalculator:
    def __init__(self, decay_factor: float = 0.90, saturation_threshold_mm: float = 180.0):
        self.decay = decay_factor
        self.threshold = saturation_threshold_mm

    def compute_asmi(self, precipitation_series: pd.Series, freq_hours: int = 4) -> pd.Series:
        step_decay = np.exp(-(freq_hours / 24.0) * (1.0 - self.decay))
        n = len(precipitation_series)
        asmi = np.zeros(n)
        current = 20.0
        precip_vals = precipitation_series.values
        for i in range(n):
            current = current * step_decay + precip_vals[i]
            asmi[i] = current
        return pd.Series(asmi, index=precipitation_series.index, name="asmi_mm")

    def estimate_saturation_percentage(self, asmi_series: pd.Series) -> pd.Series:
        pct = (asmi_series / self.threshold) * 100.0
        return pct.clip(lower=0.0, upper=100.0).rename("soil_saturation_pct")


    # Estimates saturation percentage against effective retention capacity
