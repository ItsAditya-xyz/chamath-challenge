import json
import sys
import numpy as np

# Load precomputed files so that shit doesn't go brrr during .sh runs
data = np.load("public_data_preprocessed.npz")
X_norm = data['X_norm']
y = data['y']

with open("scaling.json") as f:
    scaling = json.load(f)
means = np.array(scaling['means'])
stds = np.array(scaling['stds'])

def predict(td, mi, re):
    input_point = np.array([
        (td - means[0])/stds[0],
        (mi - means[1])/stds[1],
        (re - means[2])/stds[2]
    ])

    dists = np.linalg.norm(X_norm - input_point, axis=1)
    k = 3
    idx = np.argsort(dists)[:k]
    weights = 1 / (dists[idx] + 1e-8)
    weighted_avg = np.sum(y[idx] * weights) / np.sum(weights)
    return round(weighted_avg, 2)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Error: 3 arguments required", file=sys.stderr)
        sys.exit(1)

    td = float(sys.argv[1])
    mi = float(sys.argv[2])
    re = float(sys.argv[3])
    print(predict(td, mi, re))
