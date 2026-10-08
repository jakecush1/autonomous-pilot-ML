# Song et al. 2024: Drift prediction with a neural-network correction

- **Paper:** Song, Wang, Xiong, Cheng, Huang & Zhang, "The Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipment Based on Fully Connected Neural Network (FCNN) Embedding Model", J. Mar. Sci. Eng. 12(12):2262, 2024. doi:10.3390/jmse12122262.
- **Link:** [MDPI](https://www.mdpi.com/2077-1312/12/12/2262) (open access)
- **Read:** abstract, Fig. 1 (method overview), results, §5 conclusions and limitations. **Priority:** skim.
- **This summary:** written by Claude from the full paper (19 pp). Not Jake's own notes; check it against the paper before using it in the review.
- **Used in:** 2.2 Drift prediction · Comparative analysis · Existing approaches & limitations · Positioning

**In one line:** a physics drift model predicts where a lost, unpowered device will go, and a small neural network re-tunes that model every time the device reports its GPS position.

## Summary

- **Goal:** better search and rescue (SAR) for unmanned equipment that has lost power and is drifting. Traditional drift predictions are made once and "no longer corrected dynamically".
- **Method (hybrid: physics + learned correction):**
  1. **Physics drift model:** drift = surface current × a coefficient (about 1.2) + wind-driven "leeway". Leeway comes from the US Coast Guard LEEWAY model: drift is linear in the wind speed at 10 m, split into downwind and crosswind parts. Waves are ignored because the object is under 30 m long.
  2. **FCNN correction:** a small fully connected network (sigmoid activations) takes the reported positions and times plus the wind and current fields, and outputs two corrected coefficients: one for current (α) and one for wind (β). The loss is the mean squared distance between corrected and actual positions. The new coefficients go back into the physics model, which re-predicts the trajectory.
  3. **Search area:** Monte Carlo particles run through the corrected model give the probability that the target is inside each search cell.
- **Data:**
  - Six devices deployed southwest of the Penghu Islands (Taiwan Strait) in April 2023, giving 104 drift data points.
  - Wind at 10 m and current at 0.5 m depth come from *forecast* data, interpolated to minute resolution.
  - The data is not public.
- **Results:** the mean distance between predicted and actual track fell from **5.75 km to 0.41 km** after several position reports. The more reported points, the better the correction.
- **Limitations (§5.1–5.2):** ignores waves (which matter for bigger objects offshore). Forecast wind and current are coarse, and interpolating them adds error. Unknown disturbances (e.g. biological fouling) aren't modelled.
- **Intended use:** planning searches for lost unmanned equipment.

## Strengths and weaknesses

**Strengths**
- The only data-driven drift paper on the list, and it uses real sea trials.
- Corrects the model with the vehicle's own position reports, which is exactly what our telemetry is.
- Keeps the physics, so the model stays interpretable (two coefficients) and needs little data.
- Large accuracy gain (5.75 km down to 0.41 km).

**Weaknesses**
- Unpowered, lost equipment: no controller and no human decision.
- Small dataset: 104 points from one area in one month.
- Still relies on forecast wind and current fields, not onboard measurements.
- The output is a trajectory and a search area, not a decision.

## How it relates to our paper

**The link:** the same pattern we want for V2. The vehicle's own position reports correct a physics-style prediction, so the model learns from telemetry instead of trusting fixed coefficients.

| Section | How to use it |
|---|---|
| 2.2 Drift prediction | The data-driven / hybrid drift example, next to Dugan & Utne's physics-only one. |
| Hierarchy figure | Drift prediction × data-driven/hybrid. It's the only paper in that cell. |
| Comparative analysis: table (Rowan) | One row; see the table below. |
| Comparative analysis: Venn (Rowan) | Circle B (drift prediction) only. |
| Existing approaches & limitations (Rowan) | Even the data-driven version still depends on forecast wind and current fields, and was tested on a small dataset. |
| Positioning (Rowan) | A method idea for V2, not a competitor: it predicts *where* something drifts, not *whether a human must act*. |

> Optional idea: their correction learns only two numbers (how strongly current and wind push the object), not a whole black-box trajectory. That's a middle ground between your V1 grid and a full ML model, for example learning "how fast does the DataXplorer drift per knot of wind from each direction" from logged telemetry.

## Compared with our project

| | Song et al. 2024 | Our project |
|---|---|---|
| Vessel | Lost, unpowered unmanned equipment (<30 m) | OOR DataXplorer: powered and station-keeping |
| Situation | Drifting after a failure and needs to be found | Holding station; the pilot corrects when it's pushed outward |
| Output | Corrected drift trajectory + search-area probability | P(pilot must intervene within Δt) |
| Inputs | Reported GPS fixes, forecast wind (10 m) and current | Position, distance to station, wind speed and direction |
| Method | LEEWAY physics + an FCNN that re-tunes 2 coefficients | V1: pilot-rule grid; V2: learned from logged interventions |
| Data | 6 devices, Penghu Islands, April 2023, 104 points | Simulation + OOR's logged telemetry and interventions |
| Validation | Mean track deviation (km) | Recall, false alerts per shift, watch hours removed, against the V1 grid |
| Human role | A search team uses the predicted area | Pilot moves from 24/7 watch to on-call alerts |

## To fix in the background doc

- It's listed under "Other resources" at the end of 2.3. Move it to 2.2.
