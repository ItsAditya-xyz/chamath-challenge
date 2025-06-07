import json
import numpy as np

with open("public_cases.json") as f:
    data = json.load(f)

durations = []
miles = []
receipts = []
outputs = []

for case in data:
    inp = case['input']
    durations.append(inp['trip_duration_days'])
    miles.append(inp['miles_traveled'])
    receipts.append(inp['total_receipts_amount'])
    outputs.append(case['expected_output'])

print(f"Trip Duration: min={min(durations)}, max={max(durations)}, mean={np.mean(durations):.2f}")
print(f"Miles: min={min(miles)}, max={max(miles)}, mean={np.mean(miles):.2f}")
print(f"Receipts: min={min(receipts)}, max={max(receipts)}, mean={np.mean(receipts):.2f}")
