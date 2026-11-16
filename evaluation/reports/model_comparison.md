# Drift prediction: linear regression → LSTM → transformer

**Question:** the USV is drifting with its motor off. Given the last 60 minutes,
where will it be 60 minutes from now?

Each model outputs one thing: metres drifted east/north **exactly 60 min ahead** (motor off).
Predicted position = position now + that. It does not predict the path in between,
or anything while the motor is on. To change the horizon, edit `H` in `src/cmn/data_prep.py`.

This is **regression, not classification**: the output is a distance in metres
(east, north), so the plan's "logistic regression" became linear regression.

## Run
From the top folder of the repository. Quick start (creates `.venv` the first time, then runs every step below):
```
bash quickstart.sh
```
Or step by step:
```
python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/main.py prep          # build windows   -> data/preprocessed/windows_H60.npz
.venv/bin/python src/main.py baselines     # baselines + linear regression
.venv/bin/python src/main.py lstm          # ~1 min on CPU
.venv/bin/python src/main.py transformer   # ~3 min on CPU
.venv/bin/python src/main.py compare       # table + evaluation/results/comparison.png
```

## Data (`src/cmn/data_prep.py`)
- One sample = a moment *t* with the motor off for the 60 min before **and**
  after, no tow-speed movement (> 93 m/min), and no data gaps longer than 5 min.
- Input: 60 rows (one per minute) of `[dx, dy, wind_push_e, wind_push_n]`.
  `dx, dy` = metres moved that minute; wind is the direction it **pushes** the boat
  (`-sin(from)`, `-cos(from)` × speed).
- Target: metres moved east/north over the next 60 minutes.
- **Split by deployment, never random.** Neighbouring windows share 59 of their 60 minutes.
  | split | deployments | windows |
  |---|---|---|
  | train | Apr 17–29, May 19–Jun 6, Jun 3–17, Aug 5–14, Sep 10–22 | 23,455 |
  | val (early stopping) | Oct 3–13 | 2,289 |
  | test (only scored, never tuned on) | Oct 16–23 | 4,559 |
  | holdout (unused until the final score) | Nov 2–9, Nov 11–16 (`data/holdout/`) | — |

  May 19–Jun 6 and Jun 3–17 overlap on Jun 3–6; `build()` keeps one window per time, so those days count once.

## Models
| model | input | idea |
|---|---|---|
| no_drift | — | baseline: it stays put (sanity floor) |
| persistence | past-hour drift | baseline: next hour = last hour, no wind, no training. **The bar every model must beat** |
| linear_reg | past-hour drift, wind now, mean wind past hour | `y = A·x + c` |
| lstm | full 60-min sequence | 2-layer LSTM (64 hidden), last hidden state → (e, n) |
| transformer | full 60-min sequence | 2-layer encoder (d=64, 4 heads), sin/cos positions, mean-pool → (e, n) |

The neural nets use inputs/targets standardised with train stats, Adam (lr 1e-3), MSE loss,
early stopping on val loss (patience 10), and seed 0.

## Results (position error after 60 min, metres)
| model | test median | test p90 | test R² | val median | val p90 |
|---|---|---|---|---|---|
| no_drift | 586 | 1515 | 0.00 | 635 | 1257 |
| persistence | 294 | 570 | 0.80 | 326 | 563 |
| linear_reg | 324 | 626 | 0.77 | 237 | 456 |
| **lstm** | **257** | 510 | 0.84 | 163 | 342 |
| transformer | 272 | **489** | **0.85** | 171 | 338 |

Test median vs. persistence: linear_reg **+30 m (worse)**, lstm **−37 m**, transformer **−22 m**.

Milestone 3 (5 deployments, 16,471 training windows) scored linear_reg 318, lstm 247, transformer 246 m on the same test set:
42% more training data did not lower the test error.

## How to read the output
- **median / p90:** half (90%) of predicted positions were within this many metres of where
  the USV really was after 60 min. p90 is the "how bad can it get" number.
- **val vs test:** val (Oct 3–13) is used to decide when the nets stop training; test (Oct 16–23)
  is never trained or tuned on. **Quote test.**
- **Linear-reg weights:** `predicted east = 0.881·past_dx + 0.188·past_dy + … + 42.8`.
  Diagonal ≈ 0.86–0.88 means drift mostly continues; the off-diagonals (−0.306, +0.188) mean it turns
  clockwise. `wind_*_now` and `wind_*_mean` are nearly the same signal, so their weights partly
  cancel (+53 / −39). Don't read them one by one.
- **Epoch lines** (`epoch 3  train 0.098  val 0.065`): an epoch is one pass over the train set; the numbers are
  MSE loss in standardised units (0 = perfect, ~1 = always guessing the average drift).
  The epoch with the lowest **val** is kept (LSTM: epoch 1, transformer: epoch 2). After that, val rises while
  train falls (overfitting), and training stops after 10 epochs without improvement. `train` is the last
  batch only, so it's noisy; watch its trend.

## What it means
- **Past drift is most of the signal.** Persistence alone cuts error in half vs. no_drift.
  Drift is mostly current/tide, which changes slowly, so whatever pushed the USV last hour
  is probably still pushing it.
- **Linear regression beats persistence on val but not on test.** Its wind weights fit
  the training deployments, and Oct 16–23 behaves differently. This is why we hold out a whole
  deployment: Jake's training-set R² of 0.82 looked better than the model really is.
- **LSTM and transformer both beat persistence on test** (LSTM 13% lower median and 11% lower p90;
  transformer 8% lower median and 14% lower p90).
  Reading the minute-by-minute sequence shows them the drift *turning* and changing speed, which
  a single past-hour total can't. Persistence assumes the last hour simply repeats.
- **Transformer no better than LSTM.** With ~30k heavily-overlapping windows (≈ 500 independent hours),
  there isn't enough data for the transformer's extra capacity to help. Both overfit within a few
  epochs (best val loss at epoch 1–2), so early stopping matters.
- **p90 ≈ 490–510 m** is a candidate safety radius for "where could it be in an hour".

## Caveats / next steps
- One seed per model; the 15 m gap between LSTM and transformer, and the change since Milestone 3,
  may be inside run-to-run noise.
  Run 3–5 seeds and report mean ± std before claiming either wins.
- Val is used for early stopping, so val numbers are slightly optimistic; quote test.
- Try: H = 15/30/120, tide phase (12.42 h sin/cos) as a feature, predicting the residual
  on top of persistence, smaller/more-regularised nets, multi-step output (whole path, not just endpoint).
- Jake's `src/linear_fits/drift_prediction.py` (was `future.py`) uses `wind_from_cos` for east and `wind_from_sin` for north; compass
  sin is east, so those look swapped (and they're "from", not "push"). Worth raising with him.
