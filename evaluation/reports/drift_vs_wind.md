## Drift vs. wind — speed and direction (v2, Nov 18 2026)

**Question:** how much does wind contribute to the USV's drift?

**Script:** `src/linear_fits/drift_vs_wind.py N` (N = window in minutes; run for 1, 30, 60; the report uses 60).
Plot: `evaluation/results/linear_fits/{N}min-drift_vs_wind.png`.

**Data:** the 7 development deployments in `data/raw/`. A row is kept only if its **whole** N-minute window
is clean: no time gaps, motor off every minute, slower than 93 m/min (3 kn, else a tow), wind ≥ 1 kn.
(v1 below only checked the last minute, so gaps and motor-on minutes could slip into a window.)

### Fits (same rows for all three)
| N (min) | Rows | Speed R² | Downwind w (m/min per kn) | Downwind R² | Vector R² | Turn |
|---|---|---|---|---|---|---|
| 1 | 49,644 | 0.115 | 1.249 (4.0% of wind) | 0.225 | 0.257 | 26° clockwise |
| 30 | 33,320 | 0.109 | 1.299 (4.2%) | 0.207 | 0.237 | 24° clockwise |
| **60** | 25,640 | 0.112 | 1.310 (4.2%) | 0.204 | 0.233 | 22° clockwise |

- **speed:** `drift speed = w · wind speed + b`. Explains ~11% at every N (v1's 0.13 at N = 10 was the looser filter).
- **downwind:** only the part of the drift that goes *with* the wind, against wind speed. Current in random
  directions cancels out here, so the slope doubles (~4% of wind speed, top of the 1–4% windage rule of thumb).
- **vector:** `drift (e, n) = W · wind push (e, n) + c`. W turns the wind ~22° clockwise (Ekman/Coriolis, N. Hemisphere).

### Share of time drifting with the wind (drift within ±45° of downwind; 25% = no wind effect)
| Wind | N = 1 | N = 30 | **N = 60** | Share of minutes (N = 60) |
|---|---|---|---|---|
| 1–5 kn | 25% | 22% | 20% | 19% |
| 5–10 kn | 46% | 45% | 45% | 55% |
| 10–15 kn | 70% | 67% | 64% | 23% |
| ≥ 15 kn | 81% | 84% | 87% | 3% |
| all | 50% | 47% | 47% | 100% |

### What it means
- Below 5 kn the drift direction is no better than chance: current decides where the USV goes.
  Above 15 kn it drifts with the wind 87% of the time.
- Wind explains about a quarter of the drift; current and tide the rest. That is why past drift
  (which carries the current) is the strongest input to every model.
- For prediction, wind matters when it is windy: on the final test set (November, 73% of hours ≥ 10 kn)
  linear regression with wind beats persistence (269 m vs 305 m median), without wind it does not
  (301 m); on the calmer validation week (34% of hours ≥ 10 kn) the wind features change little
  (see `model_comparison.md`).

### Limitations
- Descriptive fits on the development set (no train/test split); neighbouring minutes overlap,
  so the 25,640 rows are far from independent.
- "With the wind" includes wind-driven current, which telemetry can't separate from windage.
- ≥ 15 kn is only 3% of minutes (a few windy periods).

---

## v1 — wind speed only (Nov 11 2026, superseded: looser cleaning, numbers above replace these)

**Question:** how much does wind speed explain USV drift speed?

**Model:** `drift_speed = w · wind_speed + b`
- `y` = drift speed (m/min), from GPS position change over N minutes
- `x` = wind speed (kn), single reading at the end of the window
- `w` = extra drift per knot of wind
- `b` = drift at zero wind — mostly current, plus a small GPS-jitter

**Data:** 1-min telemetry, motor-off rows only (~50,000 rows ≈ 35 days, the 7 deployments in `data/raw/`).
Removed: rows not exactly N min apart (file boundaries / gaps),
speeds > 93 m/min (> 3 kn — tow/transit, e.g. 2026-08-14).

### Results — sweep over time window N

| N (min) | w     | b    | R²        |
|---------|-------|------|-----------|
| 1       | 0.634 | 8.69 | 0.114     |
| 5       | 0.661 | 8.48 | 0.129     |
| **10**  | 0.656 | 8.45 | **0.131** |
| 30      | 0.598 | 8.61 | 0.111     |
| 60      | 0.508 | 8.92 | 0.085     |

**Best: N = 10, R² = 0.131.**

### What the numbers mean (N = 10)

**w ≈ 0.66 m/min per kn:** ÷ 30.87 → drift ≈ **2.1% of wind speed**.
Matches the 1–4% "windage" rule of thumb for floating objects.

**b ≈ 8.5 m/min (~0.27 kn):** drift with zero wind → mostly current/tide.
At 10 kn wind, wind adds ~6.6 m/min vs the ~8.5 baseline:
**current matters at least as much as wind.**

**R² ≈ 0.13:** wind speed explains at most ~13% of drift variation.
The rest is things the model can't see:
- current and tide (change through the day)
- wind direction (wind with vs. against current looks the same)
- leftover GPS noise

Low R² ≠ wrong model. Wind is a real but small part of drift.

**Predictions** (`0.656 × wind + 8.45`):
- 5 kn wind → ~11.7 m/min (~0.38 kn, ~700 m/h)
- 15 kn wind → ~18.3 m/min (~0.59 kn, ~1.1 km/h)

### Why R² peaks at N = 5–10

Two competing effects:
- **1 → 10 min: GPS noise drops.** N = 1 plot has scattered jitter
  spikes (40–75 m/min) that disappear by N = 5. b also drops
  8.69 → 8.48 ≈ the jitter floor (~0.3 m/min).
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