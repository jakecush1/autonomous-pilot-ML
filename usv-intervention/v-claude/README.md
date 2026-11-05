# v3-claude: one-hour drift prediction by linear regression

Claude's take on v3 (see `../v3/notes.txt`): given the USV's position, the wind, and its
drift over the past hour or two, predict where it will be in one hour. Nothing here judges
whether the position is good or bad; it only predicts the drift.

The model is one linear regression per tier of inputs:

    drift(t+1) = A · wind(t) + B · position(t) + C · drift(t) + D · drift(t-1) + c

`drift` is nm moved east and north in an hour, `wind` is its push split east/north in knots,
`position` is nm east/north of the buoy's old spot. The richest tier is used when its inputs
are known, otherwise the next one down:

| tier | inputs | used when |
|---|---|---|
| `two_past_hours` | wind, position, last hour's drift, the hour before that | drifting for 2+ hours |
| `one_past_hour` | wind, position, last hour's drift | drifting for 1 hour |
| `no_past_drift` | wind, position | motor just turned off |

## Files

```
v3-claude/
├── data/
│   ├── merge_usv_data.py      Grafana exports -> usv_hourly.csv, usv_motor_off.csv, usv_drift_samples.csv
│   ├── usv_hourly.csv         one row per hour: motor, wind, position
│   ├── usv_motor_off.csv      the hours with the motor off
│   └── usv_drift_samples.csv  one row per hour of drifting: inputs + how far it moved
├── drift_model.py             shared: input columns, fit, save/load, predict, lat/lon <-> nm
├── train_drift_model.py       fits all tiers on every sample -> drift_model.json
├── drift_model.json           the trained model (plain numbers, no pickle)
├── evaluate_models.py         compares input sets by cross-validation; prints the tables below
└── predict_drift.py           command line: position + wind (+ past positions) -> next position
```

The raw exports are read from `../v3/data/raw/` (named by `../v3/data/rename_raw.py`), so
they are not copied twice.

## Running it

From this folder, with the project venv active (`source ../../.venv/bin/activate`):

```bash
python data/merge_usv_data.py     # 1. rebuild the samples from the raw exports (run inside data/ or here)
python train_drift_model.py       # 2. fit and save drift_model.json
python evaluate_models.py         # 3. (optional) see how each input set scores
python predict_drift.py           # 4. predict; asks for the values, or pass them as flags:
python predict_drift.py --lat 37.389866 --lon -122.801815 --wind-kn 11.1 --wind-from 316 \
    --last-lat 37.392918 --last-lon -122.798615 --last2-lat 37.397702 --last2-lon -122.795347 --hours 2
```

Example output (real track from Oct 18, 02:00):

```
now: 4.32 nm from center (3.73 nm east, 2.18 nm north), wind 11.1 kn from 316 deg
last hour: drifted 0.24 nm toward 220 deg
+1 h: drift 0.17 nm toward 220 deg -> 37.38767, -122.80417  (4.15 nm from center)  [model: two_past_hours]
+2 h: drift 0.13 nm toward 209 deg -> 37.38580, -122.80549  (4.05 nm from center)  [model: two_past_hours]
```

The USV was really at 37.38834, -122.80703 after an hour (0.15 nm from the prediction) and
37.38869, -122.81272 after two (0.35 nm; it turned west). Past positions are given as
lat/lon points on the track, one and two hours back, because that is what the pilot can see.
With `--hours N` the prediction is rolled forward hour by hour, holding the wind constant.

## What changed in the data step

`../v3/data/merge_usv_data.py` only trusted the motor-power export and needed hourly rows, so the
May 20 - Jun 4 (2-hour steps) and Oct 17 - 21 (20-minute steps) exports gave 0 drift samples.
The GPS export carries an hourly "Motor Power" column for every date range, so the new
`data/merge_usv_data.py` builds the hourly table from that and resamples the wind to hourly
from whatever step it was exported at (readings inside an hour are vector-averaged; the 2-hour
readings are spread over both hours they cover). Result: 354 drift samples instead of 181,
and the 181 old ones are reproduced exactly.

| export | hours | motor off | drift samples |
|---|---|---|---|
| Apr 18 - 27 | 210 | 70 | 46 |
| May 20 - Jun 4 | 334 | 160 | 122 |
| Jun 26 | 7 | 3 | 2 |
| Aug 6 - 12 | 152 | 92 | 76 |
| Oct 3 - 12 | 194 | 85 | 59 |
| Oct 17 - 21 | 79 | 57 | 49 |

Each hour still covers the hour starting at its timestamp. "Motor off" means the hourly
average motor power is 0 W (`MOTOR_OFF_MAX_W` in the merge script). The samples also carry
the drift two hours back, the position at the start of the hour, how many hours the USV had
already been drifting, and which export each row came from (used for cross-validation).

## Results (from `evaluate_models.py`)

Score = distance in nm between the predicted and the real position after one hour.
"Leave-one-export-out" trains on five date ranges and tests on the sixth, for each of the six,
so every sample is scored by a model that never saw its dates. "Oct" trains on everything
before Sep 1 and tests on the two October exports.

Samples where the last two hours of drift are known (203 samples):

| predictor | mean | median | 80% within | Oct mean |
|---|---|---|---|---|
| no drift | 0.423 | 0.391 | 0.645 | |
| same as last hour | 0.174 | 0.145 | 0.249 | |
| wind only | 0.371 | 0.364 | 0.507 | 0.417 |
| wind + position | 0.364 | 0.346 | 0.524 | 0.421 |
| wind + last hour | 0.158 | 0.131 | 0.234 | 0.141 |
| wind + position + last hour | 0.156 | 0.132 | 0.229 | 0.147 |
| **wind + position + last two hours** | **0.153** | **0.131** | **0.212** | 0.144 |

Samples where only the last hour is known (268): wind + position + last hour scores 0.166
mean (vs 0.184 for "same as last hour"). First hour after the motor stops (354 samples, no
past drift): wind + position scores 0.349 (vs 0.440 for "no drift").

Two hours ahead, rolling the one-past-hour tier forward: 0.388 nm mean miss, vs 0.460 for
"same as last hour, twice" and 0.804 for "no drift".

What this says:

- **Last hour's drift is by far the strongest input.** Assuming the USV keeps doing what it
  just did already halves the error of ignoring drift. The regression improves on that by
  about 10-15%, mostly by damping the persistence and adding the wind.
- **Wind on its own explains less than past drift does.** Drift speed is about 5% of wind
  speed on median, but the direction and the current are not captured by wind alone.
- **Position adds very little so far** (0.158 -> 0.156). It is kept because you asked for
  it and because it is the only input that could pick up a current that varies across the
  zone, which more data may reveal. With little data a spare input costs almost nothing.
- **The two-hours-ago term helps a bit** (coefficients of about +1.1 on the last hour and
  -0.35 on the hour before: it extrapolates the trend, then damps it).
- Plain least squares beat ridge regression at every input set, so no regularization is used.

## Limits, and what data to get next

- Everything is hourly, so the model cannot see a wind shift inside the hour. The finer
  exports in `../v3/data/query_windows.md` would mainly help if the model moves to
  sub-hour steps; for the hourly model, **more days** matter more than finer steps, and
  **May 20 - Jun 4 and Oct 17 - 21 no longer need re-querying** for this purpose.
- Only 6 date ranges and 354 drift hours; nearly all drifting happens in winds under 15 kn,
  so predictions in strong wind are extrapolation.
- When new exports arrive: drop the four panels into `../v3/data/raw/`, run
  `python ../v3/data/rename_raw.py` there, then steps 1-3 above. The hourly GPS export
  (with its Motor Power column) is the one file every date range must have.
