# Legacy

Earlier work that the current code in `src/` replaced. It is kept for reference and is not maintained:
the scripts still point at the folders they used to live in, so they will not run as they are.

- `hourly_drift/` - the first drift model, built on hourly data: Grafana exports in `data/raw/`,
  the scripts that merged them, and a linear regression on the hourly drift samples.
  The 1-minute pipeline in `src/` replaced it.
- `v3-template.py` - the starting template for the drift work (an early copy of the location check).
- `merge_1min.py` - an unfinished loader for the 1-minute exports.
