> | 4 | **Song et al. 2024**, "Prediction and Dynamic Correction of Drifting Trajectory for Unmanned Maritime Equipment…", JMSE 12:2262. [MDPI](https://www.mdpi.com/2077-1312/12/12/2262) | The only data-driven drift paper you have (physics model + neural-network correction) | Abstract, method overview, results, §5 limitations | 2.2, comparison |

> [Claude] Written by Claude from the full paper (19 pp). These aren't your own notes, so check them against the paper before using them in the review.

Drift prediction for lost, unpowered unmanned equipment (search and rescue). A physics drift model predicts where the device will go, and a small neural network re-tunes that model every time the device reports its GPS position.

- **Goal:** better search and rescue for unmanned equipment that has lost power and is drifting. Traditional drift predictions are made once and "no longer corrected dynamically".
- **Method (hybrid: physics + learned correction):**
  1. **Physics drift model:** drift = surface current × a coefficient (about 1.2) + wind-driven "leeway". Leeway comes from the US Coast Guard LEEWAY model: drift is linear in the wind speed at 10 m, split into downwind and crosswind parts. Waves are ignored because the object is under 30 m long.
  2. **FCNN correction:** a small fully connected network (sigmoid activations) takes the reported positions and times plus the wind and current fields. It outputs two corrected coefficients, one for current (α) and one for wind (β). The loss is the mean squared distance between corrected and actual positions. The new coefficients go back into the physics model, which re-predicts the trajectory.
  3. **Search area:** Monte Carlo particles run through the corrected model give the probability that the target is inside each search cell.
- **Data:**
  - Six devices deployed southwest of the Penghu Islands (Taiwan Strait) in April 2023, giving 104 drift data points.
  - Wind at 10 m and current at 0.5 m depth come from *forecast* data, interpolated to minute resolution.
  - The data is not public.
- **Results:** the mean distance between the predicted and actual track fell from **5.75 km to 0.41 km** after several position reports. The more reported points, the better the correction.
- **Limitations (§5.1–5.2):**
  - Ignores waves, which matter for bigger objects offshore.
  - Forecast wind and current are coarse, and interpolating them adds error.
  - Unknown disturbances (e.g. biological fouling) aren't modelled.
- **Intended use:** planning searches for lost unmanned equipment.

- Link to us: this is the pattern we want for V2. The device's own position reports correct a physics-style prediction, so the model learns from telemetry instead of trusting fixed coefficients.

> Optional idea: their correction learns only two numbers (how strongly current and wind push the object), not a whole black-box trajectory. That's a middle ground between your V1 grid and a full ML model, for example learning "how fast does the DataXplorer drift per knot of wind from each direction" from logged telemetry.

Pros:
- The only data-driven drift paper on your list, and it uses real sea trials.
- Corrects the model with the vehicle's own position reports, which is exactly what our telemetry is.
- Keeps the physics, so the model stays interpretable (two coefficients) and needs little data.
- Large accuracy gain (5.75 km down to 0.41 km).

Cons:
- Unpowered, lost equipment: no controller and no human decision.
- Small dataset: 104 points from one area in one month.
- Relies on forecast wind and current fields, not onboard measurements.
- The output is a trajectory and a search area, not a decision.

> **[Claude] Differences to our situation** (could become a row in your comparison table):
>
> | | Song et al. 2024 | Our project |
> |---|---|---|
> | Vessel | Lost, unpowered unmanned equipment (<30 m) | OOR DataXplorer: powered and station-keeping |
> | Situation | Drifting after a failure and needs to be found | Holding station; the pilot corrects when it's pushed outward |
> | Output | Corrected drift trajectory + search-area probability | P(pilot must intervene within Δt) |
> | Inputs | Reported GPS fixes, forecast wind (10 m) and current | Position, distance to station, wind speed and direction |
> | Method | LEEWAY physics + an FCNN that re-tunes 2 coefficients | V1: pilot-rule grid; V2: learned from logged interventions |
> | Data | 6 devices, Penghu Islands, April 2023, 104 points | Simulation + OOR's logged telemetry and interventions |
> | Validation | Mean track deviation (km) | Recall, false alerts per shift, watch hours removed, against the V1 grid |
> | Human role | A search team uses the predicted area | Pilot moves from 24/7 watch to on-call alerts |
>
> **Where it goes in the background doc:** 2.2, in the data-driven / hybrid cell of your hierarchy. In the comparison it's the "physics + learned correction" example, the closest method idea to your V2.
