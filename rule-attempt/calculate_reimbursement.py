import json
import sys

with open("best_params.json", "r") as f:
    p = json.load(f)

def calculate_reimbursement(days, miles, receipts):
    total = p['per_diem'] * days
    if days == 5:
        total += p['five_day_bonus']

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

    mileage_pay = (
        p['mileage_t1'] * min(miles, p['mileage_cutoff']) +
        max(0, miles - p['mileage_cutoff']) * p['mileage_t2']
    )

    efficiency = miles / days
    if p['efficiency_low'] <= efficiency <= p['efficiency_high']:
        eff_bonus = p['efficiency_bonus']
    elif efficiency >= p['efficiency_penalty_trigger']:
        eff_bonus = p['efficiency_penalty']
    else:
        eff_bonus = 0

    total += mileage_pay + receipts_pay + eff_bonus
    return round(total, 2)

if __name__ == "__main__":
    trip_duration_days = int(sys.argv[1])
    miles_traveled = int(sys.argv[2])
    total_receipts_amount = float(sys.argv[3])

    result = calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount)
    print(result)
