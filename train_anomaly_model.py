import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Load data
df = pd.read_csv("synthetic_sensor_data.csv")

# 2. Select sensor features
features = [
    "temperature_c",
    "vibration_mm_s",
    "motor_current_a",
    "speed_rpm"
]

X = df[features]

# 3. Create model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

# 4. Train model
model.fit(X)

# 5. Predict anomalies
df["prediction"] = model.predict(X)

print(df["prediction"].value_counts())

from sklearn.metrics import classification_report, confusion_matrix

# Convert predictions to 0 and 1
df["predicted_anomaly"] = (
    df["prediction"] == -1
).astype(int)

y_true = df["simulated_anomaly"]
y_pred = df["predicted_anomaly"]

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

print("\nClassification Report:")
print(classification_report(y_true, y_pred))


import matplotlib.pyplot as plt

df["timestamp"] = pd.to_datetime(df["timestamp"])

anomalies = df[df["predicted_anomaly"] == 1]

plt.figure(figsize=(12, 5))

plt.plot(
    df["timestamp"],
    df["temperature_c"],
    label="Temperature",
    alpha=0.7
)

plt.scatter(
    anomalies["timestamp"],
    anomalies["temperature_c"],
    color="red",
    label="Detected Anomaly",
    s=25
)

plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Industrial Machine - Temperature Anomaly Detection")
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()