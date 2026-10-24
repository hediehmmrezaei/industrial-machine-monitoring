import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 1000

timestamps = pd.date_range(
    start="2026-10-01 08:00:00",
    periods=n,
    freq="min"
)

# Simulated normal operating conditions
temperature = rng.normal(45, 3, n)
vibration = rng.normal(2.0, 0.3, n)
motor_current = rng.normal(12, 1, n)
speed = rng.normal(1450, 20, n)

# Inject artificial abnormal behavior
anomaly_indices = rng.choice(
    n, size=50, replace=False
)

temperature[anomaly_indices] += 20
vibration[anomaly_indices] += 3
motor_current[anomaly_indices] += 5
speed[anomaly_indices] -= 150

df = pd.DataFrame({
    "timestamp": timestamps,
    "temperature_c": temperature,
    "vibration_mm_s": vibration,
    "motor_current_a": motor_current,
    "speed_rpm": speed
})

# For evaluation only, not for model training
df["simulated_anomaly"] = 0
df.loc[anomaly_indices, "simulated_anomaly"] = 1

df.to_csv("synthetic_sensor_data.csv", index=False)

print(df.head())
print("\nTotal records:", len(df))
print("Simulated anomalies:", df["simulated_anomaly"].sum())