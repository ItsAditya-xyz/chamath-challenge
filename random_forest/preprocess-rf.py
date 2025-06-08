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

# Save data as npz for faster loading
np.savez("public_data_rf.npz", X=np.array(X), y=np.array(y))

print("✅ Random Forest preprocessing complete.")
