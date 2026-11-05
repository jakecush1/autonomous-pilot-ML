#!/usr/bin/env python3
# Trains the v3 drift model on every drift sample in data/usv_drift_samples.csv and saves it to
# drift_model.json (one linear regression per tier of inputs, see drift_model.py).
#
# Run from this folder:   python train_drift_model.py
# Re-run it whenever data/merge_usv_data.py has produced new samples.
import pandas as pd
from drift_model import TARGET, TIERS, load_samples, fit_all_tiers, save_models, MODEL_FILE

samples = load_samples()
models = fit_all_tiers(samples)
save_models(models)

print(f"trained on {len(samples)} drift samples, saved to {MODEL_FILE}")
for name, model in models.items():
    print(f"\n{name}: {model['n_samples']} samples")
    print("  what the model learned (rows: moved east, moved north | columns: inputs)")
    table = pd.DataFrame(model["coef"], index=TARGET, columns=model["inputs"]).round(4)
    print("  " + table.to_string().replace("\n", "\n  "))
    print(f"  constant part (nm per hour east, north): {model['intercept']}")
