import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("synthetic_sensor_data.csv")

features = [
    "temperature_c",
    "vibration_mm_s",
    "motor_current_a",
    "speed_rpm"
]

# Chronological split
train_df = df.iloc[:600].copy()
validation_df = df.iloc[600:800].copy()
test_df = df.iloc[800:].copy()

train_df = train_df[
    train_df["simulated_anomaly"] == 0
]

# Keep only known-normal records for training
train_df = train_df[
    train_df["simulated_anomaly"] == 0
]

X_train = train_df[features]
X_test = test_df[features]

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

# Train only on past observations
model.fit(X_train)

# Predict only on unseen observations
import numpy as np

# Calculate anomaly scores
train_scores = model.score_samples(X_train)
test_scores = model.score_samples(X_test)

# Set threshold using the normal training data
threshold = np.percentile(train_scores, 1)

# Lower scores indicate more anomalous observations
y_pred = (test_scores < threshold).astype(int)

print("Threshold:", threshold)
print("Detected anomalies:", y_pred.sum())

y_true = test_df["simulated_anomaly"]

print("Training records:", len(train_df))
print("Test records:", len(test_df))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

print("\nClassification Report:")
print(classification_report(y_true, y_pred))

print("Training records:", len(train_df))
print("Validation records:", len(validation_df))
print("Test records:", len(test_df))

print(
    "Validation anomalies:",
    validation_df["simulated_anomaly"].sum()
)

print(
    "Test anomalies:",
    test_df["simulated_anomaly"].sum()
)