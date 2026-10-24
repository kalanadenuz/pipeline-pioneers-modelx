
# Physical Conservation in Machine Learning
Runoff volume must never exceed total input precipitation volume.

## ASMI Formulation
ASMI_t = ASMI_{t-1} * decay + P_t
where decay = exp(-(delta_t / 24) * (1 - alpha))
