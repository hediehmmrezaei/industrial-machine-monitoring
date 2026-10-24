import joblib
import pandas as pd

# Load the saved model
package = joblib.load("industrial_anomaly_model.joblib")

model = package["model"]
threshold = package["threshold"]
features = package["features"]

# New sensor reading
new_data = pd.DataFrame([{
    "temperature_c": 70.0,
    "vibration_mm_s": 5.5,
    "motor_current_a": 18.0,
    "speed_rpm": 1300
}])

# Keep the same feature order as training
X_new = new_data[features]

# Calculate anomaly score
score = model.score_samples(X_new)[0]

# Classify machine status
if score < threshold:
    status = "ANOMALY"
else:
    status = "NORMAL"

print("Anomaly Score:", round(score, 4))
print("Threshold:", round(threshold, 4))
print("Machine Status:", status)