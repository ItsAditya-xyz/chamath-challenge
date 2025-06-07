# wrote generate_results.py cuz generate_results.sh sucks

import json
from model import predict  # directly import your function

# Load private test cases
with open("private_cases.json", "r") as f:
    private_cases = json.load(f)

total_cases = len(private_cases)
print(f"📊 Processing {total_cases} test cases...")
print(f"📝 Output will be saved to private_final_results.txt")

results_file = "private_final_results.txt"

with open(results_file, "w") as f_out:
    for i, case in enumerate(private_cases, start=1):
        if i % 100 == 0:
            print(f"Progress: {i}/{total_cases} cases processed...")

        try:
            td = float(case['trip_duration_days'])
            mi = float(case['miles_traveled'])
            re = float(case['total_receipts_amount'])

            result = predict(td, mi, re)
            f_out.write(f"{result}\n")

        except Exception as e:
            print(f"Error on case {i}: {e}")
            f_out.write("ERROR\n")

print("\n✅ Results generated successfully!")
print(f"📄 Output saved to {results_file}")
