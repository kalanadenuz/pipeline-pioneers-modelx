# HydroPulse: 3-Minute Video Script & Panel Defense Guide

> **Competition:** ModelX 2.0 Hackathon · Domain 02: Climate & Disaster Risk  
> **Team:** Pipeline Pioneers (Kalana Kuruppu & Theekshana Chandrathunga)  
> **Deliverable:** 3-Minute Video Walkthrough on Real Kelani River Basin Data

---

## Part 1: Second-by-Second Video Recording Plan (0:00 to 3:00)

* **0:00 – 0:30 (Problem & The Farmer Persona):**
  * *Visual:* Photo/map of sunny vegetable plot in Hanwella; split screen with high-altitude storm over Norton Bridge.
  * *Speaker (Kalana):* "Imagine managing a two-acre commercial vegetable plot in Hanwella. You look up: sunny skies. But 50 km upstream in Norton Bridge, 180 mm of extreme rain just fell. Water takes 16 hours to arrive. Today, by the time water spills onto access roads, farmers have 45 minutes to react. Pumps submerge, tractors flood, crops rot—costing up to LKR 600,000 per family. We built HydroPulse to provide a calibrated, 16-hour advance warning."
* **0:30 – 1:05 (The Best Data Vision Architecture):**
  * *Visual:* Diagram showing NASA GPM IMERG 0.1°, Copernicus ERA5-Land SWVL1/SWVL2, and USGS SRTM 30m DEM.
  * *Speaker (Theekshana):* "To solve this, we formulated the Best Data Vision architecture. We rejected brittle web scrapers and physical IoT sensors prone to theft and drift. Instead, we pull NASA GPM microwave precipitation, Copernicus rootzone soil moisture, and USGS elevation slopes. Crucially, while NASA telemetry has a 2.5-hour downlink delay, our 16-hour wave routing window leaves an actionable 13-hour advance notice."
* **1:05 – 1:45 (Live Terminal Execution on Real Data):**
  * *Visual:* Screen recording of running `python run_pipeline.py`. Real-time logs appear in 3 seconds.
  * *Speaker (Kalana):* "Here is the system running live on real Kelani Basin flood data. In under 3 seconds, HydroPulse ingests records, verifies physical conservation laws, and computes ASMI soil memory decay. On peak storm surges, standard persistence fails with a 1.45m error. HydroBoost achieves an MAE of 0.397m—a 72.6% improvement over persistence, with a Critical Success Threat Score of 0.662."
* **1:45 – 2:20 (Interactive Dashboard & Conformal Bounds):**
  * *Visual:* Browser at `http://localhost:8000/dashboard` showing May 2024 storm wave, countdown timer (15h 42m), saturation gauge (92.4%), and 90% conformal interval bar.
  * *Speaker (Theekshana):* "Next, our web dashboard serving Biyagama farmers. For the May 2024 flood event, upstream saturation has crossed 92%, triggering an expected 0.65m local inundation. But notice: we never output a deceptive single-point guess. HydroPulse applies Inductive Conformal Prediction, guaranteeing a 90% confidence bound between 0.22m and 1.08m, validated across historical holdouts."
* **2:20 – 2:45 (Epistemic Humility & Safe-Failure Demonstration):**
  * *Visual:* Click *"Inject Latency Fault (>6h)"*. The dashboard turns amber, halts point predictions, flags `SAFE FAILURE STATE`, and widens uncertainty by ±40%.
  * *Speaker (Theekshana):* "The hardest part of AI is knowing what data cannot support. Here, we inject a live telemetry latency fault (>6h). Watch the system: it refuses to make an ungrounded guess, switches to Safe-Failure State, and broadens its uncertainty bounds by ±40%. Furthermore, if headwater rain exceeds 150mm, it flags an unmodeled dam spillway advisory."
* **2:45 – 3:00 (Actionable Farmer Alert & Impact):**
  * *Visual:* Smartphone mockup showing plain-text bilingual SMS alert with checklist.
  * *Speaker (Kalana):* "The farmer receives a direct SMS: 'Dismantle pumps and move tractors before 02:00 AM.' A 16-hour head start converts a disaster into a routine asset preservation drill, protecting millions of rupees across rural Sri Lanka."

---

## Part 2: Judge Q&A Defense Strategy

1. **"Why not deep learning (LSTM/Transformers)?"**  
   *Defense:* "In sparse-gauge tropical basins, black-box deep networks overfit and hallucinate impossible water balances (predicting runoff greater than total rainfall). HydroBoost runs in 8.6ms on CPU without GPU overhead, guarantees conservation laws, and provides complete feature interpretability."
2. **"What if upstream dams release spill gates unannounced?"**  
   *Defense:* "Satellite rain cannot see human dam gate levers. This is why we built Epistemic Humility: when 24h rain exceeds 150mm (reservoir threshold), HydroPulse triggers an explicit Dam Spillway Advisory directing farmers to sirens."
3. **"Why Conformal Prediction?"**  
   *Defense:* "Monsoonal flash floods are heavy-tailed and non-Gaussian; standard Gaussian assumptions break down. Conformal prediction is mathematically guaranteed to provide finite-sample distribution-free valid coverage (96.4% on our holdouts)."
