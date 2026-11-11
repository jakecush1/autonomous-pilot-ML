## Drift model v2: predicting 1-hour position

**Question:** given the last hour of drift and the current wind, where
will the USV be in H minutes (motor off)?

**Model:** `LinearRegression`, 2 outputs at once (east, north)
- Features (X): `past_dx`, `past_dy` (m moved over past H min),
  `wind_e`, `wind_n` (kn, "wind FROM" vector: sin → east, cos → north)
- Targets (y): `future_dx`, `future_dy` (m moved over next H min)
- Predicted position = current position + (future_dx, future_dy)

**Data:** 1-min telemetry, all files in `data/`, H = 60
Kept a row only if:
- past and future windows are exactly H min (no gaps / file joins)
- motor off for the whole past hour AND whole next hour
- past and future movement < 93 m/min × H (no tow/transit)
→ 21,076 rows (of 85,915)

### Results (TRAINING data only, not trustworthy yet)

R² = 0.830 (v1, wind speed only: 0.145)

| feature  | → east | → north |
|----------|--------|---------|
| past_dx  | 0.923  | −0.260  |
| past_dy  | 0.180  | 0.843   |
| wind_e   | −4.649 | −18.672 |
| wind_n   | −21.513| −11.131 |
intercept (east, north): (−20.9, +28.8) m/h

### What it means
- **Past drift dominates:** next hour ≈ 0.85–0.92 × last hour.
  Captures current/tide/avg wind without measuring them.
- **Off-diagonal (−0.26, +0.18) = drift turning clockwise.**
  Hypothesis: rotating tidal current / Coriolis (N. Hemisphere). Untested.
- **Wind:** ~200–250 m/h extra per 10 kn. Read with caution:
  overlaps with past drift (wind was blowing last hour too) and is
  correlated with the tide/daily cycle. Wind from N → south + west
  (right of wind, as expected in N. Hemisphere); wind_e row less clear.
- **Intercept ~36 m/h toward NW:** small, because past drift now
  carries the current (v1's b was ~480 m/h).

### Why R² = 0.83 can't be trusted yet
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
- [ ] Move one whole file (latest deployment) → `data/holdout/`.
      Don't touch until the end.
- [ ] Split remaining data **by time**: first 80% train, last 20%
      validation. Never a random split.
- [ ] Add a gap of H rows between train and validation so no
      window spans both
- [ ] Baseline: predict `future = past` (no model). Compute its error.
- [ ] Report error in **metres** (median + 90th pct), not just R²
- [ ] Convert prediction → predicted lat/lon

### Tests (run on VALIDATION, change one thing at a time)

| # | Change                                   | Median err (m) | 90th pct (m) | Keep? |
|---|------------------------------------------|----------------|--------------|-------|
| 0 | Baseline: future = past                  |                |              |   —   |
| 1 | v2 as-is (H = 60)                        |                |              |       |
| 2 | Past drift only (no wind)                |                |              |       |
| 3 | Wind only (no past drift)                |                |              |       |
| 4 | Wind averaged over past hour (rolling)   |                |              |       |
| 5 | Separate past window P = 30 (H = 60)     |                |              |       |
| 6 | + drift from 2 h ago (turning/accel.)    |                |              |       |
| 7 | + tide phase sin/cos (12.42 h)           |                |              |       |
| 8 | + station-distance filter (~10 km)       |                |              |       |
| 9 | Ridge(alpha=…) instead of LinearRegression |              |              |       |
| 10| H = 15 / 30 / 120: error vs. horizon     |                |              |   —   |

Tests 2 and 3 show how much each feature group contributes.
Test 10 isn't a "keep" decision; it shows how fast error grows.

### Final
- [ ] Pick the best settings from the table
- [ ] Retrain on train + validation
- [ ] Score ONCE on `data/holdout/` → this is the real number
- [ ] If more data arrives (new season / new station area), test
      on it before trusting the model there

### Code cleanup
- [ ] Remove `checks` debugging block
- [ ] Fix comment: `.diff(H)` = now − H min ago