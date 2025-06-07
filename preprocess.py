import json
import numpy as np

# Load data
with open("public_cases.json", "r") as f:
    data = json.load(f)

# Prepare dataset
X = []
y = []
for case in data:
    inp = case['input']
    td = float(inp['trip_duration_days'])
    mi = float(inp['miles_traveled'])
    re = float(inp['total_receipts_amount'])
    X.append([td, mi, re])
    y.append(float(case['expected_output']))

X = np.array(X)
y = np.array(y)

# Normalize features
means = X.mean(axis=0)
stds = X.std(axis=0)
X_norm = (X - means) / stds

# Save normalized dataset
np.savez("public_data_preprocessed.npz", X_norm=X_norm, y=y)

# Save scaling parameters
scaling = {
    "means": means.tolist(),
    "stds": stds.tolist()
}

with open("scaling.json", "w") as f:
    json.dump(scaling, f)

print("✅ Preprocessing complete.")
