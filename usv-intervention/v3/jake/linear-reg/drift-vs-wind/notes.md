## Drift vs. wind — simple linear regression (v1)

**Question:** how much does wind speed explain USV drift speed?

**Model:** `drift_speed = w · wind_speed + b`
- `y` = drift speed (m/min), from GPS position change over N minutes
- `x` = wind speed (kn), single reading at the end of the window
- `w` = extra drift per knot of wind
- `b` = drift at zero wind — mostly current, plus a small GPS-jitter

**Data:** 1-min telemetry, motor-off rows only (~37,000 rows ≈ 26 days).
Removed: rows not exactly N min apart (file boundaries / gaps),
speeds > 93 m/min (> 3 kn — tow/transit, e.g. 2026-08-14).

### Results — sweep over time window N

| N (min) | w     | b    | R²        |
|---------|-------|------|-----------|
| 1       | 0.692 | 8.35 | 0.125     |
| 5       | 0.728 | 8.08 | 0.144     |
| **10**  | 0.719 | 8.11 | **0.145** |
| 30      | 0.663 | 8.29 | 0.127     |
| 60      | 0.582 | 8.56 | 0.104     |

**Best: N = 10, R² = 0.145.**

### What the numbers mean (N = 10)

**w ≈ 0.72 m/min per kn:** ÷ 30.87 → drift ≈ **2.3% of wind speed**.
Matches the 1–4% "windage" rule of thumb for floating objects.

**b ≈ 8.1 m/min (~0.26 kn):** drift with zero wind → mostly current/tide.
At 10 kn wind, wind adds ~7 m/min vs the ~8 baseline:
**current matters at least as much as wind.**

**R² ≈ 0.145:** wind speed explains at most ~15% of drift variation.
The rest is things the model can't see:
- current and tide (change through the day)
- wind direction (wind with vs. against current looks the same)
- leftover GPS noise

Low R² ≠ wrong model. Wind is a real but small part of drift.

**Predictions** (`0.719 × wind + 8.11`):
- 5 kn wind → ~11.7 m/min (~0.38 kn, ~700 m/h)
- 15 kn wind → ~18.9 m/min (~0.61 kn, ~1.1 km/h)

### Why R² peaks at N = 5–10

Two competing effects:
- **1 → 10 min: GPS noise drops.** N = 1 plot has scattered jitter
  spikes (40–75 m/min) that disappear by N = 5. b also drops
  8.35 → 8.08 ≈ the jitter floor (~0.3 m/min).
- **10 → 60 min: timing mismatch grows.** Currents and drift can change 
  over an hour so this allows too many innacuracies.

### Observations from the plots
- **High wind (> 16 kn) = a few storm events**, not broad coverage.
  w is partly set by those few episodes; may change with more data.
- **Suspect points at 50–85 m/min at ~5 kn wind** (N = 5, 10): under the
  93 cap, likely tow ramp-up/down or first minutes after motor off.
  Station-distance filter should remove them.

### Limitations
- R² is on training data (no train/test split yet)
- Speed only, no direction → can't predict a position yet

### To try
- Require motor off on the previous row too`

### Next model (v2)
Add wind direction (sin/cos) + past-hour drift, predict east/north
movement (→ position in 1 h), train/test split **by time**.