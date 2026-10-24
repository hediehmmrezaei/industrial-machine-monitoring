
import pandas as pd
import joblib
from sqlalchemy import create_engine, text

# Connect to PostgreSQL
engine = create_engine(
    "postgresql+psycopg://localhost:5432/industrial_monitoring"
)

# Load saved ML model
package = joblib.load("industrial_anomaly_model.joblib")

model = package["model"]
threshold = package["threshold"]
features = package["features"]

# Read latest sensor record for Machine 1
query = """
SELECT
    reading_id,
    machine_id,
    recorded_at,
    temperature_c,
    vibration_mm_s,
    motor_current_a,
    speed_rpm
FROM sensor_readings
WHERE machine_id = 1
ORDER BY recorded_at DESC, reading_id DESC
LIMIT 1;
"""

df = pd.read_sql(query, engine)

if df.empty:
    print("No sensor readings found.")

else:
    X = df[features]

    score = model.score_samples(X)[0]

    status = (
        "ANOMALY" if score < threshold
        else "NORMAL"
    )

    print("Machine ID:", df["machine_id"].iloc[0])
    print("Recorded at:", df["recorded_at"].iloc[0])
    print("Anomaly Score:", round(score, 4))
    print("Machine Status:", status)

    # Get sensor reading ID
    reading_id = int(df["reading_id"].iloc[0])

    # SQL query to save prediction
    insert_query = text("""
        INSERT INTO anomaly_predictions
        (reading_id, anomaly_score, threshold, predicted_status)
        VALUES
        (:reading_id, :anomaly_score, :threshold, :status)
        ON CONFLICT (reading_id) DO NOTHING
    """)

    # Save prediction to PostgreSQL
    with engine.begin() as connection:
        result = connection.execute(
            insert_query,
            {
                "reading_id": reading_id,
                "anomaly_score": float(score),
                "threshold": float(threshold),
                "status": status
            }
        )

    if result.rowcount == 0:
        print("Prediction already exists. Skipped.")
    else:
        print("Prediction saved to PostgreSQL!")
