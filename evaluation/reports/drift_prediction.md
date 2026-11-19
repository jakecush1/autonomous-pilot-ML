## Drift model v2: predicting 1-hour position

**Question:** given the last hour of drift and the current wind, where
will the USV be in H minutes (motor off)?

**Model:** `LinearRegression`, 2 outputs at once (east, north)
- Features (X): `past_dx`, `past_dy` (m moved over past H min),
  `wind_e`, `wind_n` (kn, "wind FROM" vector: sin → east, cos → north)
- Targets (y): `future_dx`, `future_dy` (m moved over next H min)
- Predicted position = current position + (future_dx, future_dy)

**Data:** 1-min telemetry, all files in `data/raw/`, H = 60
Kept a row only if:
- past and future windows are exactly H min (no gaps / file joins)
- motor off for the whole past hour AND whole next hour
- past and future movement < 93 m/min × H (no tow/transit)
→ 27,480 rows (of 117,396)

### Results (TRAINING data only, not trustworthy yet)

R² = 0.819 (v1, wind speed only: 0.131)

| feature  | → east | → north |
|----------|--------|---------|
| past_dx  | 0.918  | −0.271  |
| past_dy  | 0.176  | 0.845   |
| wind_e   | −5.077 | −16.517 |
| wind_n   | −20.594| −10.818 |
intercept (east, north): (−0.4, +31.4) m/h

### What it means
- **Past drift dominates:** next hour ≈ 0.85–0.92 × last hour.
  Captures current/tide/avg wind without measuring them.
- **Off-diagonal (−0.27, +0.18) = drift turning clockwise.**
  Hypothesis: rotating tidal current / Coriolis (N. Hemisphere). Untested.
- **Wind:** ~170–210 m/h extra per 10 kn. Read with caution:
  overlaps with past drift (wind was blowing last hour too) and is
  correlated with the tide/daily cycle. Wind from N → south + west
  (right of wind, as expected in N. Hemisphere); wind_e row less clear.
- **Intercept ~31 m/h toward N:** small, because past drift now
  carries the current (v1's b was ~480 m/h).

### Why R² = 0.82 can't be trusted yet
1. Scored on training data
2. Rows overlap (neighbours share 59/60 min) → near-copies in training
3. No baseline: "next hour = last hour" may score almost as well

### Plots
- Predicted vs actual (east, north): dots on the diagonal = good;
  flatter than the diagonal = model too cautious
- Error histogram (m): median and 90th percentile.
  **90th pct = candidate safety radius** for the autopilot

---

## TODO

### Lesson 3: honest testing (do before any tuning)
- [x] Move one whole file (latest deployment) → `data/holdout/`.
      Don't touch until the end. *(Nov 2–9 and Nov 11–16; scored once on Nov 18)*
- [x] Split remaining data **by time**: first 80% train, last 20%
      validation. Never a random split. *(by deployment: train Apr–Oct 13, validation Oct 16–23)*
- [ ] Add a gap of H rows between train and validation so no
      window spans both
- [x] Baseline: predict `future = past` (no model). Compute its error. *(persistence, `src/models/linear_reg.py`)*
- [x] Report error in **metres** (median + 90th pct), not just R²
- [ ] Convert prediction → predicted lat/lon

### Tests (run on VALIDATION, change one thing at a time)

| # | Change                                   | Median err (m) | 90th pct (m) | Keep? |
|---|------------------------------------------|----------------|--------------|-------|
| 0 | Baseline: future = past                  | 294            | 570          |   —   |
| 1 | v2 as-is (H = 60)                        | 320            | 629          |  yes  |
| 2 | Past drift only (no wind)                | 322            | 645          |  no   |
| 3 | Wind only (no past drift)                |                |              |       |
| 4 | Wind averaged over past hour (rolling)   |                |              |       |
| 5 | Separate past window P = 30 (H = 60)     |                |              |       |
| 6 | + drift from 2 h ago (turning/accel.)    |                |              |       |
| 7 | + tide phase sin/cos (12.42 h)           |                |              |       |
| 8 | + station-distance filter (~10 km)       |                |              |       |
| 9 | Ridge(alpha=…) instead of LinearRegression |              |              |       |
| 10| H = 15 / 30 / 120: error vs. horizon     |                |              |   —   |

Rows 0–2 are on the validation week (Oct 16–23), from `src/models/linear_reg.py`, whose v2 also
uses the mean wind over the past hour (6 features). Tests 3–10 were not run.
Tests 2 and 3 show how much each feature group contributes.
Test 10 isn't a "keep" decision; it shows how fast error grows.

### Final
- [ ] Pick the best settings from the table
- [ ] Retrain on train + validation
- [x] Score ONCE on `data/holdout/` → this is the real number
      *(Nov 18: 269 m median, 476 m 90th pct; without wind 301 / 587; persistence 305 / 572)*
- [ ] If more data arrives (new season / new station area), test
      on it before trusting the model there

### Code cleanup
- [ ] Remove `checks` debugging block
- [ ] Fix comment: `.diff(H)` = now − H min ago