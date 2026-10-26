
# Physical Conservation in Machine Learning
Runoff volume must never exceed total input precipitation volume.

## ASMI Formulation
ASMI_t = ASMI_{t-1} * decay + P_t
where decay = exp(-(delta_t / 24) * (1 - alpha))

Alpha calibration: alpha=0.90 corresponds to approximately 7-14 day retention half-life.

Topological lags: 14h (Deraniyagala), 16h (Kitulgala), 22h (Castlereigh), 24h (Norton Bridge).
