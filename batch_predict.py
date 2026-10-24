import pandas as pd
import joblib
from sqlalchemy import create_engine, text
engine = create_engine(
    "postgresql+psycopg://localhost:5432/industrial_monitoring"
)

package = joblib.load("industrial_anomaly_model.joblib")

model = package["model"]
threshold = package["threshold"]
features = package["features"]

# Read all sensor records
query = """
SELECT
    s.reading_id,
    s.machine_id,
    s.recorded_at,
    s.temperature_c,
    s.vibration_mm_s,
    s.motor_current_a,
    s.speed_rpm
FROM sensor_readings AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM anomaly_predictions AS p
    WHERE p.reading_id = s.reading_id
)
ORDER BY s.recorded_at;
"""

df = pd.read_sql(query, engine)

if df.empty:
    print("No sensor data found.")

else:
    X = df[features]

    # Predict all records together
    df["anomaly_score"] = model.score_samples(X)

    df["predicted_status"] = df["anomaly_score"].apply(
        lambda score: "ANOMALY"
        if score < threshold
        else "NORMAL"
    )

    print(df[[
        "machine_id",
        "recorded_at",
        "anomaly_score",
        "predicted_status"
    ]])

    print("\nPrediction Summary:")
    print(df["predicted_status"].value_counts())

    insert_query = text("""
    INSERT INTO anomaly_predictions
    (reading_id, anomaly_score, threshold, predicted_status)
    VALUES
    (:reading_id, :anomaly_score, :threshold, :status)
    ON CONFLICT (reading_id) DO NOTHING
""")

saved_count = 0

with engine.begin() as connection:
    for _, row in df.iterrows():
        result = connection.execute(
            insert_query,
            {
                "reading_id": int(row["reading_id"]),
                "anomaly_score": float(row["anomaly_score"]),
                "threshold": float(threshold),
                "status": row["predicted_status"]
            }
        )

        saved_count += result.rowcount

print("\nNew predictions saved:", saved_count)