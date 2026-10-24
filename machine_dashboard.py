
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine(
    "postgresql+psycopg://localhost:5432/industrial_monitoring"
)

# Read machine data and ML predictions
query = """
SELECT
    s.recorded_at,
    s.temperature_c,
    s.vibration_mm_s,
    p.predicted_status
FROM sensor_readings AS s
JOIN anomaly_predictions AS p
    ON s.reading_id = p.reading_id
WHERE s.machine_id = 1
ORDER BY s.recorded_at, s.reading_id;
"""

df = pd.read_sql(query, engine)

if df.empty:
    print("No monitoring data found.")

else:
    print(df)

    # Calculate monitoring summary
    total_readings = len(df)
    anomaly_count = (df["predicted_status"] == "ANOMALY").sum()
    latest_status = df["predicted_status"].iloc[-1]

    print("\nMachine Monitoring Summary")
    print("Total readings:", total_readings)
    print("Anomalies detected:", anomaly_count)
    print("Latest machine status:", latest_status)

    # Filter anomalies
    anomalies = df[df["predicted_status"] == "ANOMALY"]

    # Create one figure with two charts
    fig, axes = plt.subplots(
        2, 1,
        figsize=(11, 8),
        sharex=True
    )

    # Temperature chart
    axes[0].plot(
        df["recorded_at"],
        df["temperature_c"],
        marker="o",
        label="Temperature"
    )

    axes[0].scatter(
        anomalies["recorded_at"],
        anomalies["temperature_c"],
        color="red",
        s=100,
        label="Anomaly",
        zorder=5
    )

    axes[0].set_ylabel("Temperature (°C)")
    axes[0].set_title("Temperature Monitoring")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Vibration chart
    axes[1].plot(
        df["recorded_at"],
        df["vibration_mm_s"],
        marker="o",
        label="Vibration"
    )

    axes[1].scatter(
        anomalies["recorded_at"],
        anomalies["vibration_mm_s"],
        color="red",
        s=100,
        label="Anomaly",
        zorder=5
    )

    axes[1].set_ylabel("Vibration (mm/s)")
    axes[1].set_xlabel("Time")
    axes[1].set_title("Vibration Monitoring")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    # Dashboard summary
    summary_text = (
        f"Total Readings: {total_readings}   |   "
        f"Anomalies: {anomaly_count}   |   "
        f"Latest Status: {latest_status}"
    )

    fig.suptitle(
        "Paper Rewinder - Machine Monitoring Dashboard",
        fontsize=15,
        fontweight="bold",
        y=0.98
    )

    fig.text(
        0.5,
        0.925,
        summary_text,
        ha="center",
        fontsize=11
    )

    # Reserve space for dashboard title and summary
    fig.tight_layout(rect=[0, 0, 1, 0.87])

    plt.show()
