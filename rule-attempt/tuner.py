import json
import random
import copy
import concurrent.futures
import multiprocessing

# Load public_cases.json once
with open("public_cases.json", "r") as f:
    cases = json.load(f)

test_cases = [
    (c["input"]["trip_duration_days"], c["input"]["miles_traveled"], c["input"]["total_receipts_amount"], c["expected_output"])
    for c in cases
]

# --- Rule-based model ---
def model(p, days, miles, receipts):
    total_per_diem = p['per_diem'] * days
    if days == 5:
        total_per_diem += p['five_day_bonus']

    # Receipts logic
    if days == 1:
        receipts_pay = receipts * p['receipts_multiplier_1day']
        receipts_pay = min(receipts_pay, p['receipts_cap_1day'])

    elif days >= 9:
        receipts_capped = min(receipts, p['receipts_cap_long'])
        receipts_pay = receipts_capped * p['receipts_multiplier_long']

    elif 2 <= days <= 8:
        if receipts <= p['receipts_split_point']:
            receipts_pay = receipts * p['receipts_r1']
        else:
            receipts_pay = (
                p['receipts_split_point'] * p['receipts_r1'] +
                (receipts - p['receipts_split_point']) * p['receipts_r2']
            )

    # Mileage calculation
    mileage_pay = (
        p['mileage_t1'] * min(miles, p['mileage_cutoff']) +
        max(0, miles - p['mileage_cutoff']) * p['mileage_t2']
    )

    # Efficiency bonus
    efficiency = miles / days
    if p['efficiency_low'] <= efficiency <= p['efficiency_high']:
        eff_bonus = p['efficiency_bonus']
    elif efficiency >= p['efficiency_penalty_trigger']:
        eff_bonus = p['efficiency_penalty']
    else:
        eff_bonus = 0

    total = total_per_diem + mileage_pay + receipts_pay + eff_bonus
    return round(total, 2)

# Scoring function
def score_model(p):
    total_error = 0
    for days, miles, receipts, expected in test_cases:
        prediction = model(p, days, miles, receipts)
        total_error += abs(prediction - expected)
    return total_error / len(test_cases)

# Much smarter search space
bounds = {
    'per_diem': (80, 100),
    'five_day_bonus': (40, 60),

    'receipts_multiplier_1day': (0.5, 0.9),
    'receipts_cap_1day': (800, 1200),

    'receipts_cap_long': (800, 1200),
    'receipts_multiplier_long': (0.4, 0.7),

    'receipts_split_point': (800, 1400),
    'receipts_r1': (0.6, 0.8),
    'receipts_r2': (0.05, 0.4),

    'mileage_t1': (0.3, 0.5),
    'mileage_t2': (0.2, 0.4),
    'mileage_cutoff': (250, 600),

    'efficiency_low': (150, 200),
    'efficiency_high': (190, 250),
    'efficiency_bonus': (10, 60),
    'efficiency_penalty': (-100, -20),
    'efficiency_penalty_trigger': (300, 400),
}

mutation_ranges = {k: (v[1] - v[0]) for k, v in bounds.items()}

def random_params():
    return {k: random.uniform(*bounds[k]) for k in bounds}

def mutate_params(params, mutation_scale=0.1):
    mutated = copy.deepcopy(params)
    for key in mutated:
        delta = random.uniform(-1, 1) * (mutation_ranges[key] * mutation_scale)
        mutated[key] += delta
        mutated[key] = max(bounds[key][0], min(bounds[key][1], mutated[key]))
    return mutated

def worker(args):
    base_params, mutation_scale, explore_chance = args

    if random.random() < explore_chance:
        candidate = random_params()
    else:
        candidate = mutate_params(base_params, mutation_scale)

    score = score_model(candidate)
    return (score, candidate)

if __name__ == "__main__":

    cpu_workers = multiprocessing.cpu_count()
    print(f"Using {cpu_workers} CPU cores")

    best_params = random_params()
    best_score = score_model(best_params)

    total_iterations = 10_000_000
    batch_size = cpu_workers * 8

    for iteration in range(0, total_iterations, batch_size):

        if iteration < 500_000:
            mutation_scale = 0.2
            explore_chance = 0.2
        elif iteration < 2_000_000:
            mutation_scale = 0.1
            explore_chance = 0.1
        else:
            mutation_scale = 0.05
            explore_chance = 0.05

        tasks = [(best_params, mutation_scale, explore_chance)] * batch_size

        with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_workers) as executor:
            results = executor.map(worker, tasks)

            for score, candidate in results:
                if score < best_score:
                    best_score = score
                    best_params = candidate
                    print(f"\n🎯 New Best at iter {iteration}: Score = {best_score:.4f}")
                    with open("best_params.json", "w") as f:
                        json.dump(best_params, f, indent=2)

        if iteration % 100000 == 0 and iteration != 0:
            print(f"🔄 Iteration {iteration} — Current best: {best_score:.2f}")
