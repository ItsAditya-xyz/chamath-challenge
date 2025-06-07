import json
from calculate_reimbursement import calculate_reimbursement

# Load test cases
with open('public_cases.json', 'r') as f:
    test_cases = json.load(f)
    


with open('best_params.json', 'r') as f:
    best_params = json.load(f)
    print(best_params)
    


results = []
total_error = 0
exact_matches = 0
close_matches = 0
max_error = 0

for i, case in enumerate(test_cases, start=1):
    input_data = case['input']
    expected_output = case['expected_output']

    try:
        actual_output = calculate_reimbursement(
            input_data['trip_duration_days'],
            input_data['miles_traveled'],
            input_data['total_receipts_amount']
        )

        error = abs(actual_output - expected_output)
        total_error += error

        if error < 0.01:
            exact_matches += 1
        if error < 1.0:
            close_matches += 1

        if error > max_error:
            max_error = error

        results.append((i, input_data, expected_output, actual_output, error))

    except Exception as e:
        print(f"Error on case {i}: {e}")

# Results Summary
successful_runs = len(results)
avg_error = total_error / successful_runs
num_cases = len(test_cases)

print("✅ Evaluation Complete!\n")
print("📈 Results Summary:")
print(f"  Total test cases: {num_cases}")
print(f"  Successful runs: {successful_runs}")
print(f"  Exact matches (±$0.01): {exact_matches} ({exact_matches/num_cases*100:.1f}%)")
print(f"  Close matches (±$1.00): {close_matches} ({close_matches/num_cases*100:.1f}%)")
print(f"  Average error: ${avg_error:.2f}")
print(f"  Maximum error: ${max_error:.2f}\n")

score = avg_error * 100 + (num_cases - exact_matches) * 0.1
print(f"🎯 Your Score: {score:.2f} (lower is better)\n")

# Show top 10 high error cases
results_sorted = sorted(results, key=lambda x: x[4], reverse=True)

print("💡 Top 10 high-error cases:")
for case in results_sorted[:10]:
    idx, input_data, expected, actual, error = case
    print(f"  Case {idx}: {input_data['trip_duration_days']} days, {input_data['miles_traveled']} miles, ${input_data['total_receipts_amount']} receipts")
    print(f"    Expected: ${expected:.2f}, Got: ${actual:.2f}, Error: ${error:.2f}")
