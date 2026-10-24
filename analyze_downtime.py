import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine(
    "postgresql+psycopg://localhost:5432/industrial_monitoring"
)

# Read downtime events and machine names
query = """
SELECT
    m.machine_name,
    d.reason,
    d.start_time,
    d.end_time,
    EXTRACT(EPOCH FROM (d.end_time - d.start_time)) / 60
        AS downtime_minutes
FROM downtime_events AS d
JOIN machines AS m
    ON d.machine_id = m.machine_id
ORDER BY d.start_time;
"""

df = pd.read_sql(query, engine)

print(df)

summary = (
    df.groupby("machine_name")["downtime_minutes"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTotal Downtime by Machine:")
print(summary)

stop_analysis = (
    df.groupby("machine_name")
    .agg(
        number_of_stops=("downtime_minutes", "count"),
        total_downtime=("downtime_minutes", "sum"),
        average_stop_duration=("downtime_minutes", "mean")
    )
    .round(2)
)

print("\nMachine Stop Analysis:")
print(stop_analysis)

# Planned production time: 8 hours
planned_production_minutes = 480

stop_analysis["availability_percent"] = (
    (planned_production_minutes - stop_analysis["total_downtime"])
    / planned_production_minutes
) * 100

stop_analysis["availability_percent"] = (
    stop_analysis["availability_percent"].round(2)
)

print("\nMachine Availability:")
print(stop_analysis[
    ["total_downtime", "availability_percent"]
])

import matplotlib.pyplot as plt

summary.plot(kind="bar", figsize=(9, 5))

plt.title("Total Machine Downtime")
plt.xlabel("Machine")
plt.ylabel("Downtime (minutes)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()

