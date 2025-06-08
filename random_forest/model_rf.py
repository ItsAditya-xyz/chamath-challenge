import json
import sys
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load data
data = np.load("public_data_rf.npz")
X = data['X']
y = data['y']

# Train model
model = RandomForestRegressor(
    n_estimators=500, 
    max_depth=15,  # control overfitting
    random_state=42
)
model.fit(X, y)

# Save trained model to file
joblib.dump(model, "rf_model.pkl")

print("✅ Random Forest model trained and saved.")
