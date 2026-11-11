# Predicting Remote Intervention for a Station-Keeping USV

Predict, from live telemetry, whether a remote pilot will need to intervene with an uncrewed surface vehicle (USV) within a future time horizon, so the pilot can be alerted on demand instead of kept on continuous watch.

Course project for SENG 474, University of Victoria.

## Overview

Open Ocean Robotics (OOR) operates the DataXplorer, a USV that must stay within 10 nautical miles (nm) of a retired weather buoy's position. It mostly drifts with its motor off, and a pilot watches it 24/7 although a course correction is needed only every two to three hours.

The project so far:

- **V1: Location check (complete).** A rule-based check of the USV's current position.
- **V2: One-hour drift prediction (Milestone 3).** Given the last hour of a drifting USV's movement and wind, predict where it will be in one hour. Linear regressions show what drives the drift; four models (persistence, linear regression, LSTM, transformer) are then compared on a deployment they never saw.
- **Next (Milestone 4).** Turn the predicted position into an alert for the pilot.

One command runs everything: see [Quick start](#quick-start). The longer description is under [Project background](#project-background).

## Illustrative sample

**Input:** the last 60 minutes of a drifting USV, one row per minute: metres moved east, metres moved north, and the wind's push east and north.

**Output:** how far it will move east and north over the next 60 minutes. The predicted position is the position now plus that movement.

An example from the test deployment, Oct 19 at 21:15. In the past hour the USV had moved 774 m east and 555 m north, and it was slowing down.

| | Movement over the next hour (east, north) | Distance from the real position |
|---|---|---|
| Persistence (next hour = last hour) | (774, 555) m | 609 m |
| LSTM | (460, 353) m | 238 m |
| What really happened | (283, 194) m | |

The LSTM reads the hour minute by minute, so it noticed the slowdown. Persistence assumes the last hour repeats.

## Prerequisites

- Python 3.13 (other recent versions may work; PyTorch does not always support the newest one)
- `bash` (macOS or Linux; on Windows use Git Bash or WSL)
- An internet connection the first time, to install the packages
- No GPU is needed

The packages are pinned in `requirements.txt`: numpy, pandas, scikit-learn, matplotlib, torch and pyproj.

## Installation

```bash
git clone https://github.com/jakecush1/autonomous-pilot-ML.git
cd autonomous-pilot-ML
```

The quick start below creates the Python environment and installs the packages by itself. To do it by hand instead:

```bash
python3.13 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Quick start

```bash
bash quickstart.sh
```

This sets up the environment the first time, then runs every step in order. It takes about 5 minutes on a laptop CPU.

| Step | What it runs | What you should see |
|---|---|---|
| `fits` | Both linear regressions, for every window N (1, 5, 10, 30, 60 min) and every horizon H (1, 30, 60 min) | Each fit printed with its R², and the plots in `evaluation/results/linear_fits/`. These are the numbers under [What drives the drift?](#what-drives-the-drift-linear-regression) |
| `prep` | Cuts the telemetry in `data/raw/` into 60-minute motor-off windows | The number of windows in each split |
| `baselines` | No drift, persistence and linear regression | Their error on the validation and test deployments |
| `lstm`, `transformer` | Trains and scores each neural network | The loss per epoch, then the error; the trained models go to `output/` |
| `compare` | Puts all the scores together | The results table, and the chart `evaluation/results/comparison.png`. These are the numbers under [Four models on an unseen deployment](#four-models-on-an-unseen-deployment) |

To use another Python version, put `PYTHON=` in front, for example `PYTHON=python3.12 bash quickstart.sh`.

**Running one part.** Name the steps you want:

```bash
bash quickstart.sh fits              # only the linear regressions
bash quickstart.sh prep lstm         # rebuild the windows, then train the LSTM
```

**One linear regression with your own horizon or window.** The number is in minutes. Each script prints its fit, saves its plot, and opens the plot in a window; close the window to finish.

```bash
source .venv/bin/activate
python src/linear_fits/drift_prediction.py 30    # past drift + wind -> movement over the next 30 minutes (default 60)
python src/linear_fits/drift_vs_wind.py 5        # wind speed -> drift speed over 5 minutes (default 10)
```

**V1 location check.** It asks for the USV's latitude and longitude and the wind direction.

```bash
python src/location_check/location_check.py
```

## Results

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

![Drift speed against wind speed, N = 10 minutes](evaluation/results/linear_fits/10min-drift_plot.png)

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

![Predicted against actual drift, H = 1 minute](evaluation/results/linear_fits/1min_drift_r2_0.93.png)

H = 30 minutes:

![Predicted against actual drift, H = 30 minutes](evaluation/results/linear_fits/30min_drift_r2_0.91.png)

H = 60 minutes:

![Predicted against actual drift, H = 60 minutes](evaluation/results/linear_fits/60min_drift_r2_0.83.png)

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

![Median and 90th-percentile error by model](evaluation/results/comparison.png)

More detail is in the write-ups in `evaluation/reports/` and in the Milestone 3 report in `docs/3_Solution_Jake_Rowan`.

## Project background

### Background

Open Ocean Robotics (OOR) operates the DataXplorer, a USV that reports marine weather data for NOAA in place of the discontinued Station 46012 buoy. The vessel's only hard operating constraint is to remain within 10 nautical miles (nm) of the buoy's former position.

A remote pilot currently watches the vessel 24/7, roughly 1,095 eight-hour shifts per year, even though a corrective navigation command is needed only every two to three hours. This project asks whether that decision can be predicted from telemetry, turning a continuous watch into an on-call, alert-driven one.

The model is **advisory only**. It decides *whether* a pilot is needed, never *what* the pilot should do, and all navigation decisions stay with a human.

### Problem Definition

Let $p_0$ be the station point and $p$ the vehicle's reported position, each a latitude–longitude pair. Local wind is given by speed $v \ge 0$ (knots) and direction $\theta \in [0^\circ, 360^\circ)$, measured clockwise from true North as the direction the wind blows *from*.

A state is $\mathbf{s} = (p, p_0, v, \theta)$. Let $d(\mathbf{s})$ be the geodesic distance from $p$ to $p_0$; the operating constraint is $d(\mathbf{s}) \le R = 10$ nm.

For a horizon $\Delta t > 0$, the goal is a decision function

$$f: \mathcal{S} \rightarrow \{0, 1\}$$

where $f(\mathbf{s}) = 1$ if a pilot must issue a corrective command within $[t, t + \Delta t]$ to keep the vehicle inside $R$, and $0$ otherwise.

**Building block: drift prediction.** Before deciding *when* a pilot must act, we predict *where* the drifting vessel will be. Given the last $H$ minutes of its movement and the wind (motor off), a function

$$g: \mathbb{R}^{H \times 4} \rightarrow \mathbb{R}^{2}$$

predicts how far it will move east and north over the next $H$ minutes. We use $H = 60$. The predicted position can then be checked against the 10 nm limit.

### Approach

**V1: Location check (complete).** A rule-based check of the USV's current position. It converts latitude and longitude to nautical miles east and north of the station and flags a position that is outside 10 nm, in the traffic lane (more than 6.5 nm east), within 1 nm of the limit, or more than 6 nm from the centre. It also reports whether the wind is pushing the USV toward the centre or away from it. It looks only at the present position and makes no prediction. Code: `src/location_check`.

**V2: One-hour drift prediction (Milestone 3).** It has two parts:

1. **Linear regressions** (`src/linear_fits`): simple fits that show what drives the drift and how the prediction horizon $H$ changes the result.
2. **Model comparison** (`src/cmn`, `src/models`, `src/evaluate`): persistence ("next hour = last hour"), linear regression, an LSTM and a transformer, trained on three deployments and tested on a deployment they never saw.

**Next (Milestone 4): from predicted position to an alert.** Turn the predicted position into a time until the vessel reaches the 10 nm limit and a probability that the pilot must act, and score the models once on the held-out November deployment.

**Out of scope:** reinforcement learning for direct navigation control. A V2 model could later serve as a safety monitor for such an agent.

### Evaluation

Drift predictions are scored by endpoint error: the distance in metres between the predicted and the real position after 60 minutes, reported as the median and the 90th percentile.

The intervention model will be compared against the V1 location check on:

- **Interventions caught:** the fraction of real interventions the model alerts on in advance (recall).
- **Unnecessary alerts:** false alerts raised per shift.
- **Watch time removed:** hours of continuous monitoring the alert system replaces.

Errors are asymmetric. A missed intervention risks the station-keeping constraint, while a false alert costs one page, so recall on real interventions is weighted above alert precision.

## File structure

- `src` - the code: our learned ML models, which test and run multiple different models, and the location checker
- `data` - the telemetry the models learn from
- `output` - the trained models
- `evaluation` - results (scores and charts) and write-ups
- `docs` - written documents for each stage of the project, and summaries of related literature
- `legacy` - earlier work that the code in `src` replaced

```
autonomous-pilot-ML/
├── README.md
├── requirements.txt                # the packages, pinned
├── quickstart.sh                   # one command: set up, then run everything
├── data/
│   ├── raw/                        # five deployments of 1-minute telemetry (Apr-Oct 2026)
│   ├── preprocessed/               # the 60-minute windows built from them (made by the `prep` step)
│   └── holdout/                    # a sixth deployment (Nov 2-9), kept unseen for the final test
├── src/
│   ├── main.py                     # runs every step, or the ones you name
│   ├── cmn/                        # shared: loading, cleaning, windows, split, error in metres
│   ├── linear_fits/                # linear regressions: what drives drift, and the effect of the horizon H
│   ├── models/                     # persistence, linear regression, LSTM, transformer
│   ├── evaluate/                   # results table and chart
│   └── location_check/             # V1: rule-based check of the current position
├── output/                         # trained LSTM and transformer
├── evaluation/
│   ├── results/                    # scores (results.json), comparison chart, linear-fit plots
│   └── reports/                    # write-ups of the linear fits and of the model comparison
├── docs/
│   ├── 1_Proposal_Jake_Rowan/      # Milestone 1 report (LaTeX + PDF)
│   ├── 2_Background_Jake_Rowan/    # Milestone 2 report (LaTeX + PDF)
│   ├── 3_Solution_Jake_Rowan/      # Milestone 3 report (LaTeX + PDF), and its first draft
│   ├── summaries/                  # notes on the papers we reviewed
│   ├── notes/                      # planning notes
│   └── examples/                   # course manuals and sample reports
└── legacy/                         # the earlier hourly drift model and templates
```

## Milestones

- [x] Milestone 1: project proposal
- [x] Milestone 2: background and related work
- [x] V1 location check
- [x] Milestone 3: proposed solution (one-hour drift prediction)
- [ ] Milestone 4: evaluation, including the held-out November deployment
- [ ] Milestone 5: 3-minute talk

## Team

- Jake Cushway, University of Victoria
- Rowan Hall, University of Victoria

Individual contributions are tracked through assigned issues and commit history in this repository. AI use for Milestone 3 is declared in the report's footnote.

## Citation

```bibtex
@misc{cushway2026usvdrift,
  author = {Cushway, Jake and Hall, Rowan},
  title  = {Predicting One-Hour Drift for a Station-Keeping USV},
  year   = {2026},
  note   = {SENG 474 course project, University of Victoria},
  url    = {https://github.com/jakecush1/autonomous-pilot-ML}
}
```

## License

Released under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
