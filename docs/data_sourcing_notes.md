
# NASA GPM IMERG V06
Calibrated microwave & IR satellite precipitation estimates.
Downlink latency: 2-4 hours.

## ECMWF ERA5-Land
Volumetric soil water layer 1 (0-7cm) and layer 2 (7-28cm).
Surface runoff rasters at 0.1 degree.

## Licensing & Open Science
NASA GPM: Free open science.
Copernicus CDS: Open Access.
SRTM: Public Domain.

## Catchment Masking
Bounding box: (6.70N, 7.25N, 79.85E, 80.60E) encapsulates total 2,292 km² drainage area.

Short gaps (<3h) imputed via forward-fill; preserves physical time continuity.

4-hour frequency chosen: balances satellite pass frequency with computational responsiveness.

Milestone 1 verified: spatial clipping to Kelani Basin bounding box complete.

## Sensor Artifacts & Cloud Occlusion
Optical sensors fail under monsoonal cloud decks. Microwave radar bypasses clouds.

Telemetry latency: GPM Early Run (2h), Late Run (14h), Final Run (3 months). Early run used for real-time inference.
