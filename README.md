# Predicting Remote Intervention for a Station-Keeping USV

Predict, from live telemetry, whether a remote pilot will need to intervene with an uncrewed surface vehicle (USV) within a future time horizon, so the pilot can be alerted on demand instead of kept on continuous watch.

Course project for SENG 474, University of Victoria.

## Overview

Open Ocean Robotics (OOR) operates the DataXplorer, a USV that must stay within 10 nautical miles (nm) of a retired weather buoy's position. It mostly drifts with its motor off, and a pilot watches it 24/7 although a course correction is needed only every two to three hours.

The project so far:

- **V1: Location check (complete).** A rule-based check of the USV's current position.
- **V2: One-hour drift prediction (Milestone 3).** Given the last hour of a drifting USV's movement and wind, predict where it will be in one hour. Linear regressions show what drives the drift; four models (persistence, linear regression, LSTM, transformer) are then compared on a deployment they never saw.
- **Evaluation (Milestone 4).** Evaluate the quality and validity of the prediction models

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
