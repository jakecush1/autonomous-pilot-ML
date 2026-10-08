# Dugan & Utne 2024: Time to grounding (TTG), a drift-based risk indicator

- **Paper:** Dugan & Utne, "Development of a risk indicator for ship drifting groundings", PSAM17 & ASRAM2024, Sendai, 2024 (NTNU).
- **Link:** [PDF](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf) (open access)
- **Read:** all (10 pp). **Priority:** must read.
- **This summary:** written by Claude from the full paper. Not Jake's own notes; check it against the paper before using it in the review.
- **Used in:** 1.1 History · 2.1 Geofencing · 2.2 Drift prediction · Comparative analysis · Existing approaches & limitations · Positioning

**In one line:** if this ship lost propulsion right now, how long until it drifts aground? Recomputed along the voyage as an early warning, it's the *time* version of our question.

## Summary

- **Goal:** an early-warning risk indicator for *drifting groundings*, where a ship loses propulsion and wind, waves and current push it ashore. Motivated by real accidents (Amoco Cadiz 1978, the Viking Sky near-miss in 2019, and others).
- **Method (physics-based, no learning). At each timestamp:**
  1. Take the ship's position from the voyage data recorder.
  2. Look up historical forecast wind, waves and current for that place and time.
  3. Compute drift speed and direction from a force balance, then add the sea current. The force balance is the Sørgård & Vada model: wind drag + wave drift force − form drag − wave damping, iterated until it settles.
  4. Treat drift direction as uncertain: a normal distribution around the predicted direction (σ = 20°), sampled ±45° either side.
  5. For each angle, divide the distance to the nearest hazard by the drift speed to get a time. Hazards are chart polygons shallower than 1.5× the ship's draft. A probability-weighted sum gives the expected TTG.
- **Older approaches (their §2.1):** earlier risk assessments used a fixed drift speed (e.g. uniform 1–3 m/s) and simply set drift direction equal to wind direction.
- **Data / case study:**
  - RV Gunnerus (36 m NTNU research ship), one voyage from Ålesund to Trondheim, Norway, Nov 3–4 2022 (the Fig. 1 caption says 2023).
  - 34 points about 30 min apart.
  - Wind and waves from MyWaveWAM800m (800 m grid, hourly); currents from NorKyst.
- **Results:**
  - TTG varies a lot along the voyage. The minimum was **7 minutes**, at point 8 in Hustadvika, an exposed stretch with shoals where the Viking Sky nearly grounded. Inland it was much higher.
  - A line at **1 hour** marks the average repair time after losing propulsion. TTG often drops below it, so a failure at those points would be critical.
  - Stronger wind means faster drift. But wave direction is often out of line with wind direction, so drift direction doesn't simply follow the wind.
- **Validation:** none against real groundings. The paper only shows how TTG varies along one voyage.
- **Limitations (§5.2):** only one drift model was used. That model was validated on 250–270 m tankers, with wind damping ignored, which may not hold for small vessels. It also assumes constant weather while drifting, so it's less reliable beyond a few hours.
- **Intended use:** helping vessel traffic service (VTS) operators prioritise high-risk ships, placing emergency tugs, and as an input to risk-based controllers on autonomous ships.
- **Key argument (§5.1):** anti-grounding control systems "use the distance to shore to express grounding risk level". TTG is better because "using the distance to ground does not incorporate the expected drift motion of the ship".

## Strengths and weaknesses

**Strengths**
- Simple, cheap and reproducible: it uses commonly available data and simple hydrodynamics.
- Models the uncertainty in drift direction instead of guessing one straight line.
- Updates continuously along the voyage, so it's dynamic rather than a one-off assessment.
- Argues directly that distance alone is a weak risk signal.

**Weaknesses**
- Not validated against real drift or real groundings.
- The drift model comes from large tankers and may not transfer to small vessels.
- Assumes constant weather, so it's unreliable over long horizons.
- Needs forecast current and wave data plus the ship's hull dimensions. We only have wind and position.
- Gives an expected time, not a probability within a window, and has no human decision in the loop.

## How it relates to our paper

**The link:** replace "ground" with "the 10 nm boundary" and TTG is close to our problem. It warns *before* the limit and accounts for drift instead of distance alone. Their 1-hour repair-time line plays the same role as the proposal's Δt = 1 h.

| Section | How to use it |
|---|---|
| 1.1 History (Jake) | Its intro lists drifting-ship accidents (Amoco Cadiz 1978, Selendang Ayu 2004, Viking Sky 2019) and says the IMO made vessel traffic services (VTS) mandatory to monitor ships. That's a pre-ML root of "humans watching vessels for drift". If you use it, cite the reports it references. |
| 2.1 Geofencing | The evidence against distance-only rules: control systems use "the distance to shore", but distance "does not incorporate the expected drift motion". |
| 2.2 Drift prediction | The main physics-based, time-to-event drift paper. |
| Hierarchy figure | Drift prediction × physics-based. |
| Comparative analysis: table (Rowan) | One row; see the table below. |
| Comparative analysis: Venn (Rowan) | Overlap of B (drift) and C (risk), since it's a drift-based risk indicator. |
| Existing approaches & limitations (Rowan) | Supports "physics-based drift models rely on forecast oceanographic data" (NorKyst, MyWave), plus the limitations above. |
| Positioning (Rowan) | Work we *build on*: the same early-warning idea, but ours is a probability within Δt, learned from telemetry, with pilot intervention as the label. |

## Compared with our project

| | Dugan & Utne 2024 | Our project |
|---|---|---|
| Vessel | RV Gunnerus: 36 m crewed research ship | OOR DataXplorer |
| What goes wrong | Hypothetical loss of propulsion, then drifting aground | Wind pushes the vessel toward the 10 nm limit |
| Hazard | Shoals and land from nautical charts | The 10 nm boundary around Station 46012 |
| Output | Expected time to grounding (TTG) | P(pilot must intervene within Δt) |
| Inputs | Position, forecast wind, waves and current, water depth, hull size | Position, distance to station, wind speed and direction |
| Method | Physics drift model + probabilistic drift direction | V1: pilot-rule grid; V2: learned from logged interventions |
| Data | Historical forecasts along one voyage, about 30 min steps | Live telemetry |
| Validation | None (shows how TTG varies along one voyage) | Recall, false alerts per shift, watch hours removed, against the V1 grid |
| Human role | VTS operator could prioritise ships (proposed) | Pilot moves from 24/7 watch to on-call alerts |

## To fix in the background doc

- The 2.2 link is labelled "Monte Carlo", but the paper doesn't use Monte Carlo.
- "Predictive Drift Models - calculate probability of exceeding boundary in next *t*" isn't what TTG computes: TTG is an expected time. The probability-within-a-window version is *our* contribution.
