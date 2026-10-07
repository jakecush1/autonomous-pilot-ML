> | 2 | **Dugan & Utne 2024**, "Development of a risk indicator for ship drifting groundings", PSAM17. [PDF](https://www.iapsam.org/PSAM17/program/Papers/PSAM17&ASRAM2024-1377.pdf) | Time-to-event early warning built from drift; argues that distance alone is a weak signal. Replace "ground" with "10 nm boundary" | **All** (10 pp) | 2.2, comparison, positioning |

> [Claude] Written by Claude from the full paper (10 pp). These aren't your own notes, so check them against the paper before using them in the review.

A risk indicator called "time to grounding" (TTG): if this ship lost propulsion right now, how long until it drifts aground? It's recomputed along the voyage as an early warning.

Their output is really "how long until it's too late", which is the *time* version of our question.

- **Goal:** an early-warning risk indicator for *drifting groundings*, where a ship loses propulsion and wind, waves and current push it ashore. Motivated by real accidents (Amoco Cadiz 1978, the Viking Sky near-miss in 2019, and others).
- **Method (physics-based, no learning). At each timestamp:**
  1. Take the ship's position from the voyage data recorder.
  2. Look up historical forecast wind, waves and current for that place and time.
  3. Compute the drift speed and direction from a force balance, then add the sea current. The force balance is the Sørgård & Vada model: wind drag + wave drift force − form drag − wave damping, iterated until it settles.
  4. Treat the drift direction as uncertain: a normal distribution around the predicted direction (σ = 20°), sampled ±45° either side.
  5. For each angle, divide the distance to the nearest hazard by the drift speed to get a time. Hazards are chart polygons shallower than 1.5× the ship's draft. A probability-weighted sum of the times gives the expected TTG.
- **Older approaches (their §2.1):** earlier risk assessments used a fixed drift speed (e.g. uniform 1–3 m/s) and simply set the drift direction equal to the wind direction.
- **Case study:**
  - RV Gunnerus, a 36 m NTNU research ship, on one voyage from Ålesund to Trondheim, Norway, Nov 3–4 2022. The Fig. 1 caption says 2023, so check which is right.
  - 34 points about 30 min apart.
  - Wind and waves from MyWaveWAM800m (800 m grid, hourly); currents from NorKyst.
- **Results:**
  - TTG varies a lot along the voyage. The minimum was **7 minutes**, at point 8 in Hustadvika, an exposed stretch with shoals where the Viking Sky nearly grounded. Inland it was much higher.
  - They draw a line at **1 hour**, the average repair time after a loss of propulsion. TTG often drops below that line, so a failure at those points would be critical.
  - Stronger wind means faster drift. But wave direction is often out of line with wind direction, so the drift direction doesn't simply follow the wind.
- **Validation:** none against real groundings. The paper only shows how TTG varies along one voyage.
- **Intended use:** helping VTS (vessel traffic service) operators prioritise high-risk ships, placing emergency tugs, and as an input to risk-based controllers on autonomous ships.
- **Key argument (§5.1):** anti-grounding control systems "use the distance to shore to express grounding risk level". TTG is better because "using the distance to ground does not incorporate the expected drift motion of the ship".

- This is the argument against geofencing for us: replace "ground" with "the 10 nm boundary". Distance from station alone ignores where the vessel is heading.

> Optional idea: their 1-hour repair-time line is basically a Δt. "TTG < 1 h" is close to "boundary breach likely within the hour", which matches the proposal's Δt = 1 h example. That gives you a positioning sentence: TTG gives an expected time from a physics model, while we estimate the probability that a pilot is needed within Δt, learned from logged telemetry.

Pros:
- Simple, cheap and reproducible: it uses commonly available data and simple hydrodynamics.
- Models the uncertainty in drift direction instead of guessing one straight line.
- Updates continuously along the voyage, so it's dynamic rather than a one-off assessment.
- Argues directly that distance alone is a weak risk signal.

Cons:
- Not validated against real drift or real groundings.
- The drift model was only validated on 250–270 m tankers, and wind damping was ignored, which may not hold for small vessels.
- Assumes wind and weather stay constant while drifting, so it's less reliable beyond a few hours.
- Needs forecast current and wave data plus the ship's hull dimensions. We only have wind and position.
- Gives an expected time, not a probability within a window, and has no human decision in the loop.

> **[Claude] Differences to our situation** (could become a row in your comparison table):
>
> | | Dugan & Utne 2024 | Our project |
> |---|---|---|
> | Vessel | RV Gunnerus: 36 m crewed research ship | OOR DataXplorer |
> | What goes wrong | Hypothetical loss of propulsion, then drifting aground | Wind pushes the vessel toward the 10 nm limit |
> | Hazard | Shoals and land from nautical charts | The 10 nm boundary around Station 46012 |
> | Output | Expected time to grounding (TTG) | P(pilot must intervene within Δt) |
> | Inputs | Position, forecast wind, waves and current, water depth, hull size | Position, distance to station, wind speed and direction |
> | Method | Physics drift model + probabilistic drift direction | V1: pilot-rule grid; V2: learned from logged interventions |
> | Data | Historical forecasts along one voyage, about 30 min steps | Live telemetry |
> | Validation | None (shows how TTG varies along one voyage) | Recall, false alerts per shift, watch hours removed, against the V1 grid |
> | Human role | VTS operator could prioritise ships (proposed) | Pilot moves from 24/7 watch to on-call alerts |
>
> **Where it goes in the background doc:** 2.2, as the physics-based drift / time-to-event paper. Use it in the comparison as the evidence that distance alone (the geofence rule) is a weak signal, and in Positioning as work you build on. The link label in 2.2 says "Monte Carlo", but the paper doesn't use Monte Carlo, so fix the label.
