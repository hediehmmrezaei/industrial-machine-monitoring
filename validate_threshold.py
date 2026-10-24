import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score

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

# Train only on known-normal observations
train_df = train_df[
    train_df["simulated_anomaly"] == 0
]

X_train = train_df[features]
X_val = validation_df[features]

y_val = validation_df["simulated_anomaly"]

model = IsolationForest(
    n_estimators=100,
    contamination="auto",
    random_state=42
)

model.fit(X_train)

train_scores = model.score_samples(X_train)
val_scores = model.score_samples(X_val)

for percentile in [1, 3, 5]:

    threshold = np.percentile(
        train_scores, percentile
    )

    y_pred = (
        val_scores < threshold
    ).astype(int)

    precision = precision_score(
        y_val, y_pred, zero_division=0
    )

    recall = recall_score(
        y_val, y_pred, zero_division=0
    )

    f1 = f1_score(
        y_val, y_pred, zero_division=0
    )

    print(f"\nPercentile: {percentile}")
    print(f"Threshold: {threshold:.4f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1-score: {f1:.3f}")

    from sklearn.metrics import confusion_matrix, classification_report

# Select threshold based on validation results
best_percentile = 1

best_threshold = np.percentile(
    train_scores,
    best_percentile
)

# Evaluate on test data
X_test = test_df[features]
y_test = test_df["simulated_anomaly"]

test_scores = model.score_samples(X_test)

test_predictions = (
    test_scores < best_threshold
).astype(int)

print("\nSelected Threshold:", best_threshold)

print("\nTest Confusion Matrix:")
print(confusion_matrix(y_test, test_predictions))

print("\nTest Classification Report:")
print(classification_report(y_test, test_predictions))


import joblib

model_package = {
    "model": model,
    "threshold": float(best_threshold),
    "features": features
}

joblib.dump(
    model_package,
    "industrial_anomaly_model.joblib"
)

print("Model saved successfully!")