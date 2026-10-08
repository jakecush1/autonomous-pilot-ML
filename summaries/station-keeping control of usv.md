# Sarda et al. 2016: Station-keeping control of a small USV in wind and current

- **Paper:** Sarda, Qu, Bertaska & von Ellenrieder, "Station-keeping control of an unmanned surface vehicle exposed to current and wind disturbances", Ocean Engineering 127 (2016) 305–324. Bib key: `sarda2016station`.
- **Link:** [arXiv](https://arxiv.org/pdf/1702.04941) (open access)
- **Read:** abstract, §I–II, the §VII results tables, §VIII conclusions. Skip §III–VI (the maths). **Priority:** must read.
- **This summary:** written by Claude from the arXiv version (44 pp). Not Jake's own notes; check it against the paper before using it in the review.
- **Used in:** Intro · 2.1 Feedback loops · 2.1 Geofencing (contrast) · Comparative analysis

**In one line:** a control-law paper on making a small USV hold a fixed position *and* heading against wind and current, tested on the water. No human in the loop and no prediction.

## Summary

- **Goal:** hold position and heading at the same time on a small, light USV, and compare three feedback controllers with and without wind feedforward.
- **Vehicle:** WAM-V USV16, twin inflatable hulls, about 4 m and 180 kg, with two azimuthing electric thrusters (±45°). Four actuators for three degrees of freedom makes it *overactuated*. Sensors: GPS/IMU (about 1 m accuracy), compass, and an ultrasonic anemometer sampling at 1 Hz.
- **Method:**
  - Build a 3-DOF model of the boat from sea trials (bollard pull, acceleration, circle and zigzag tests).
  - Test three feedback controllers: nonlinear PD (the baseline), backstepping, and sliding mode.
  - **Wind feedforward:** use the measured wind speed and direction to estimate the wind force and cancel it *before* the boat is pushed off, instead of waiting for a position error.
- **§II mini-survey (the part to cite):**
  - Most nonlinear USV control work uses feedback linearisation, backstepping, or sliding mode.
  - Validation is "often limited to numerical simulation or small-scale experiments, rather than full-scale sea trials".
  - Most station-keeping work is on underactuated boats and holds position only, "as if it was anchored".
  - Wind feedforward "still has not been widely explored", and wind-force models are built for large ships.
- **Data / experiments:**
  - Calm sections of the Intracoastal Waterway, Dania Beach, FL. The boat can't handle more than sea state 1, 15 kn of wind or 0.2 m waves, so there were no open-ocean tests.
  - Each run lasted 700 s (about 12 min) in roughly 4–5 kn of wind.
  - Location 1 was sheltered, with the boat facing into the disturbance. Location 2 was harsher, with the disturbance at 90° to the heading.
  - Currents were **not measured** (there was no sensor for them); the only current information was tide data from a station about 4 km away.
- **Results:**
  - Location 1: mean position error 0.4–1.2 m, mean heading error 4–12°.
  - Location 2: mean position error 1.0–2.6 m, mean heading error 13–18°.
  - Sliding mode was best overall (lowest heading error). Feedforward didn't add much to it, but it did help PD and backstepping when the wind was side-on.
  - Holding heading trades off against holding position: sliding mode had the *highest* position error at Location 1 but the best heading.
  - A single anemometer is enough to measure the wind on a boat this small.
- **Intended use:** tasks that need a steady platform for seconds to minutes (acoustic or camera localisation, launching and recovering AUVs).

## Strengths and weaknesses

**Strengths**
- Real on-water trials, not only simulation.
- Uses the same kind of inputs we have: GPS position, plus wind speed and direction from one onboard sensor.
- §II is a ready-made survey of station-keeping control.

**Weaknesses**
- Holds position to within about a metre for about 12 minutes; says nothing about hours or days.
- Calm, sheltered water only. 15 kn is the vehicle's wind limit, and the proposal's example day has 22 kn.
- Currents weren't measured, even though the authors say they hurt performance.
- No human and no prediction: the controller reacts to the current error and can't say whether help will be needed later.

## How it relates to our paper

**The link:** this is the "*how* a vessel holds station" line of work that the proposal sets aside as a different problem. Its finding that wind is "a major source of disturbance" for light USVs with large windage areas supports wind speed and direction as our main inputs.

| Section | How to use it |
|---|---|
| Abstract / 1. Introduction | Already cited in the proposal intro. Keep that framing: control = how to hold station; our project = deciding when a human has to act. |
| 1.1 History (Jake) | Minor: §I lists what USVs are used for (patrol, environmental monitoring, mapping, oceanographic research), with references, if you need "why USVs matter". |
| 2.1 Feedback loops | The representative continuous feedback controller. Cite §II for "station-keeping control is mostly validated in simulation or small-scale trials". |
| 2.1 Geofencing | Contrast: a controller corrects continuously at metre scale, while a geofence/watch-circle rule only triggers at a boundary. |
| Hierarchy figure | Station-keeping control × physics-based. |
| Comparative analysis: table (Rowan) | The "control law" row; see the table below. Key contrast: metres and minutes, no human. |
| Comparative analysis: Venn (Rowan) | Circle A (station keeping) only. |
| Positioning (Rowan) | Not work we build on, but the wind-disturbance finding supports our choice of features. |

## Compared with our project

| | Sarda et al. 2016 | Our project |
|---|---|---|
| Vessel | WAM-V USV16: 4 m, 180 kg, two azimuthing thrusters | OOR DataXplorer |
| Question | *How* to hold position and heading | *When* a pilot needs to act |
| Scale | About 1 m of error over 700 s runs | 10 nm zone over hours |
| Inputs | Position, heading, measured wind (feedforward) | Position, distance to station, wind speed and direction |
| Output | Thruster commands | P(pilot must intervene within Δt) |
| Method | Physics model + nonlinear control laws | V1: pilot-rule grid; V2: learned from logged interventions |
| Environment | Calm inland waterway, ≤15 kn wind, currents not measured | Open ocean at Station 46012 |
| Human role | None during runs (a handheld remote switches between manual and autonomous) | Pilot moves from 24/7 watch to on-call alerts |

## To fix in the background doc

- It's listed under "Weather optimal positioning" as "(another)", but it isn't a weather-optimal positioning paper. Move it to Feedback loops. The real weather-optimal positioning paper is its ref [53]: Kjerstad et al., IFAC CAMS 2010.
