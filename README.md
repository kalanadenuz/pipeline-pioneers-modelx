# HydroPulse: Early-Warning Flood Intelligence Engine

ModelX 2.0 Hackathon | Domain 02: Climate & Disaster Risk
Team: Pipeline Pioneers

## Architecture Overview
Coupling satellite precipitation, antecedent soil moisture, and topological elevation.

## Offline Reproducibility
Pipeline supports 100% offline self-contained execution via pre-cached physical datasets.

### Data Cleaning Protocol
Bilinear spatial interpolation and forward-fill imputation with strict null-flagging.

- **Physical Conservation Gate:** Enforces that surface runoff never exceeds input precipitation mass.

- **Latency QA:** Telemetry freshness evaluated on every ingestion cycle.

- **ASMI Soil Memory:** Multi-day exponential decay (alpha = 0.90) modeling saturation transition.

- **Feature Pipeline:** 26 physical features combining ASMI memory, topological lags, and interaction terms.

### Benchmark Models
Evaluated against Naive Persistence and Standard Linear Lag baselines.
