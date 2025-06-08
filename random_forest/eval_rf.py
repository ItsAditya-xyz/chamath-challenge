# eval_rf.py — for evaluating Random Forest model

import json
import numpy as np
import joblib

# Load model
model = joblib.load("rf_model.pkl")

# Prediction function for compatibility
def predict(td, mi, re):
    return round(model.predict([[td, mi, re]])[0], 2)

# Load data
with open("public_cases.json", "r") as f:
    data = json.load(f)

results = []
total_error = 0
exact_matches = 0
close_matches = 0
max_error = 0

for i, case in enumerate(data, 1):
    input_data = case['input']
    expected_output = case['expected_output']

    td = float(input_data['trip_duration_days'])
    mi = float(input_data['miles_traveled'])
    re = float(input_data['total_receipts_amount'])

    actual_output = predict(td, mi, re)
    error = abs(actual_output - expected_output)

    total_error += error
    if error < 0.01:
        exact_matches += 1
    if error < 1.0:
        close_matches += 1
    if error > max_error:
        max_error = error

    results.append((i, td, mi, re, expected_output, actual_output, error))

avg_error = total_error / len(data)
score = avg_error * 100 + (len(data) - exact_matches) * 0.1

# Summary
print("✅ Evaluation Complete!\n")
print(f"📈 Results Summary:")
print(f"  Total test cases: {len(data)}")
print(f"  Exact matches (±$0.01): {exact_matches} ({exact_matches/len(data)*100:.1f}%)")
print(f"  Close matches (±$1.00): {close_matches} ({close_matches/len(data)*100:.1f}%)")
print(f"  Average error: ${avg_error:.2f}")
print(f"  Maximum error: ${max_error:.2f}")
print(f"\n🎯 Your Score: {score:.2f} (lower is better)")

# Optional: print top 5 worst cases
results.sort(key=lambda x: -x[-1])
print("\nTop 5 worst cases:")
for res in results[:5]:
    i, td, mi, re, exp, act, err = res
    print(f"  Case {i}: Days={td}, Miles={mi}, Receipts={re}")
    print(f"    Expected: ${exp:.2f}, Got: ${act:.2f}, Error: ${err:.2f}")
