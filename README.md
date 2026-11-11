# Predicting Remote Intervention for a Station-Keeping USV

Predict, from live telemetry, whether a remote pilot will need to intervene with an uncrewed surface vehicle (USV) within a future time horizon, so the pilot can be alerted on demand instead of kept on continuous watch.

Course project for SENG 474, University of Victoria.

## File structure

- `docs` - written documents for each stage of the project
- `summaries` - summaries of related literature
- `usv-intervention`
  - `solution` - our learned ML models, which test and run multiple different models
  - `v1_location_check` - a checker for the quality of a drifting USV's position

```
autonomous-pilot-ML/
├── docs/
│   ├── 1_Proposal_Jake_Rowan/      # Milestone 1 report (LaTeX + PDF)
│   ├── 2_Background_Jake_Rowan/    # Milestone 2 report (LaTeX + PDF)
│   └── examples/                   # course manuals and sample reports
├── summaries/                      # notes on the papers we reviewed
├── usv-intervention/
│   ├── v1_location_check/          # V1: rule-based check of the current position
│   └── solution/                   # V2: one-hour drift prediction (Milestone 3)
│       ├── data/                   # five deployments of 1-minute telemetry (Apr-Oct 2026)
│       ├── data_holdout/           # a sixth deployment (Nov 2-9), kept unseen for the final test
│       ├── jake/linear-reg/        # linear regressions: what drives drift, and the effect of the horizon H
│       └── rowan/                  # pipeline: data prep, baselines, LSTM, transformer, comparison
│           └── docs/3/             # Milestone 3 report (LaTeX + PDF)
├── requirements.txt
└── update.sh                       # commit-and-push helper
```

## Background

Open Ocean Robotics (OOR) operates the DataXplorer, a USV that reports marine weather data for NOAA in place of the discontinued Station 46012 buoy. The vessel's only hard operating constraint is to remain within 10 nautical miles (nm) of the buoy's former position.

A remote pilot currently watches the vessel 24/7, roughly 1,095 eight-hour shifts per year, even though a corrective navigation command is needed only every two to three hours. This project asks whether that decision can be predicted from telemetry, turning a continuous watch into an on-call, alert-driven one.

The model is **advisory only**. It decides *whether* a pilot is needed, never *what* the pilot should do, and all navigation decisions stay with a human.

## Problem Definition

Let $p_0$ be the station point and $p$ the vehicle's reported position, each a latitude–longitude pair. Local wind is given by speed $v \ge 0$ (knots) and direction $\theta \in [0^\circ, 360^\circ)$, measured clockwise from true North as the direction the wind blows *from*.

A state is $\mathbf{s} = (p, p_0, v, \theta)$. Let $d(\mathbf{s})$ be the geodesic distance from $p$ to $p_0$; the operating constraint is $d(\mathbf{s}) \le R = 10$ nm.

For a horizon $\Delta t > 0$, the goal is a decision function

$$f: \mathcal{S} \rightarrow \{0, 1\}$$

where $f(\mathbf{s}) = 1$ if a pilot must issue a corrective command within $[t, t + \Delta t]$ to keep the vehicle inside $R$, and $0$ otherwise.

**Building block: drift prediction.** Before deciding *when* a pilot must act, we predict *where* the drifting vessel will be. Given the last $H$ minutes of its movement and the wind (motor off), a function

$$g: \mathbb{R}^{H \times 4} \rightarrow \mathbb{R}^{2}$$

predicts how far it will move east and north over the next $H$ minutes. We use $H = 60$. The predicted position can then be checked against the 10 nm limit.

## Approach

**V1: Location check (complete).** A rule-based check of the USV's current position. It converts latitude and longitude to nautical miles east and north of the station and flags a position that is outside 10 nm, in the traffic lane (more than 6.5 nm east), within 1 nm of the limit, or more than 6 nm from the centre. It also reports whether the wind is pushing the USV toward the centre or away from it. It looks only at the present position and makes no prediction. Code: `usv-intervention/v1_location_check/usv2.py`.

**V2: One-hour drift prediction (current work, Milestone 3).** Code: `usv-intervention/solution`. It has two parts:

1. **Linear regressions** (`jake/linear-reg`): simple fits that show what drives the drift and how the prediction horizon $H$ changes the result.
2. **Model comparison** (`rowan`): persistence ("next hour = last hour"), linear regression, an LSTM and a transformer, trained on three deployments and tested on a deployment they never saw.

**Next (Milestone 4): from predicted position to an alert.** Turn the predicted position into a time until the vessel reaches the 10 nm limit and a probability that the pilot must act, and score the models once on the held-out November deployment.

**Out of scope:** reinforcement learning for direct navigation control. A V2 model could later serve as a safety monitor for such an agent.

## Results so far

### What drives the drift? (linear regression)

**Wind speed alone explains little.** The fit is `drift speed = w · wind speed + b` on motor-off minutes, with drift speed measured over a window of N minutes.

| N (min) | w (m/min per kn) | b (m/min) | R² |
|---|---|---|---|
| 1 | 0.692 | 8.35 | 0.125 |
| 5 | 0.728 | 8.08 | 0.144 |
| **10** | 0.719 | 8.11 | **0.145** |
| 30 | 0.663 | 8.29 | 0.127 |
| 60 | 0.582 | 8.56 | 0.104 |

- Wind speed explains at most 15% of the variation in drift speed. A 10-minute window is best: shorter windows carry GPS noise, and over longer ones the wind and current change.
- The slope is about 2.3% of the wind speed.
- With no wind the USV still drifts at about 8 m/min (0.26 kn), so current matters at least as much as wind.

![Drift speed against wind speed, N = 10 minutes](usv-intervention/solution/jake/linear-reg/drift-vs-wind/10min-drift_plot.png)

**Past drift plus wind predicts much better, and the horizon H matters.** The fit predicts the movement east and north over the next H minutes from the movement over the past H minutes and the wind vector.

| H (min) | R² | Median error (m) | 90th percentile (m) | Samples |
|---|---|---|---|---|
| 1 | 0.93 | 2 | 4 | 35,974 |
| 30 | 0.91 | 87 | 194 | 27,332 |
| 60 | 0.83 | 256 | 549 | 21,076 |

- The longer the horizon, the weaker the fit, because wind and current have longer to change.
- We keep H = 60 because a pilot needs about an hour of warning.
- At H = 60 the next hour's drift is 0.84–0.92 of the last hour's, turned slightly clockwise. Past drift captures current and tide without measuring them.

H = 1 minute:

![Predicted against actual drift, H = 1 minute](usv-intervention/solution/jake/linear-reg/drift-prediction/1min_drift_r2%3A0.93.png)

H = 30 minutes:

![Predicted against actual drift, H = 30 minutes](usv-intervention/solution/jake/linear-reg/drift-prediction/30min_drift_r2%3A0.91.png)

H = 60 minutes:

![Predicted against actual drift, H = 60 minutes](usv-intervention/solution/jake/linear-reg/drift-prediction/v2_H60_r2_0.83.png)

These numbers are measured on the same data the fits were trained on, so they are optimistic. The next table is the test on unseen data.

### Four models on an unseen deployment

Position error after 60 minutes on the test deployment (Oct 16–23), which no model saw during training:

| Model | Median (m) | 90th percentile (m) | R² |
|---|---|---|---|
| No drift (stays put) | 586 | 1515 | 0.00 |
| Persistence (next hour = last hour) | 294 | 570 | 0.80 |
| Linear regression | 318 | 631 | 0.77 |
| LSTM | 247 | 497 | 0.85 |
| **Transformer** | **246** | **477** | **0.86** |

- Persistence already halves the error of assuming no drift.
- Linear regression does not beat persistence on unseen data: its R² of 0.83 on training data falls to 0.77.
- The LSTM and transformer both beat persistence by about 16%, and are tied with each other.

![Median and 90th-percentile error by model](usv-intervention/solution/rowan/outputs/comparison.png)

More detail is in `usv-intervention/solution/rowan/README.md` and in the Milestone 3 report in `usv-intervention/solution/rowan/docs/3`.

## Evaluation

Drift predictions are scored by endpoint error: the distance in metres between the predicted and the real position after 60 minutes, reported as the median and the 90th percentile.

The intervention model will be compared against the V1 location check on:

- **Interventions caught:** the fraction of real interventions the model alerts on in advance (recall).
- **Unnecessary alerts:** false alerts raised per shift.
- **Watch time removed:** hours of continuous monitoring the alert system replaces.

Errors are asymmetric. A missed intervention risks the station-keeping constraint, while a false alert costs one page, so recall on real interventions is weighted above alert precision.

## Running the code

**Model comparison (quick start).** The script creates its own environment on first use, then runs data preparation, the baselines, both neural networks and the comparison. It takes about 5 minutes on a laptop CPU and uses Python 3.13 (set `PYTHON=` to use another version).

```bash
git clone https://github.com/jakecush1/autonomous-pilot-ML.git
cd autonomous-pilot-ML/usv-intervention/solution/rowan
bash quickstart.sh
```

**Linear regression by horizon.** The horizon `H` (minutes) is set at the top of the file.

```bash
cd autonomous-pilot-ML
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt matplotlib
cd usv-intervention/solution/jake/linear-reg/drift-prediction
python future.py
```

**V1 location check.** It asks for the USV's latitude and longitude and the wind direction.

```bash
python usv-intervention/v1_location_check/usv2.py
```

## Milestones

- [x] Milestone 1: project proposal
- [x] Milestone 2: background and related work
- [x] V1 location check
- [ ] Milestone 3: proposed solution (one-hour drift prediction)
- [ ] Milestone 4: evaluation, including the held-out November deployment
- [ ] Milestone 5: 3-minute talk

## Team

- Jake Cushway, University of Victoria
- Rowan Hall, University of Victoria

Individual contributions are tracked through assigned issues and commit history in this repository. AI use for Milestone 3 is declared in the report's footnote.

## License

Released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
