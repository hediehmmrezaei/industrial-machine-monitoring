
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from streamlit_autorefresh import st_autorefresh

# ----------------------------------
# 1. Streamlit page configuration
# ----------------------------------

st.set_page_config(
    page_title="Industrial Machine Monitoring",
    layout="wide"
)

st.title("Industrial Machine Monitoring Dashboard")
st.write("Machine condition monitoring using Machine Learning")
if st.button("🔄 Refresh Data"):
    st.rerun()

# ----------------------------------
# 2. Connect to PostgreSQL
# ----------------------------------

engine = create_engine(
    "postgresql+psycopg://localhost:5432/industrial_monitoring"
)
machines_query = """
SELECT machine_id, machine_name
FROM machines
ORDER BY machine_id;
"""

machines_df = pd.read_sql(machines_query, engine)

selected_machine = st.selectbox(
    "Select Machine",
    options=machines_df["machine_id"].tolist(),
    format_func=lambda machine_id: machines_df.loc[
        machines_df["machine_id"] == machine_id,
        "machine_name"
    ].iloc[0]
)

# ----------------------------------
# 3. Read sensor data and predictions
# ----------------------------------

query = """
SELECT
    s.recorded_at,
    s.temperature_c,
    s.vibration_mm_s,
    p.predicted_status
FROM sensor_readings AS s
JOIN anomaly_predictions AS p
    ON s.reading_id = p.reading_id
WHERE s.machine_id = :machine_id
ORDER BY s.recorded_at, s.reading_id;
"""

st_autorefresh(
    interval=30 * 1000,
    key="machine_dashboard_refresh"
)

df = pd.read_sql(
    text(query),
    engine,
    params={"machine_id": int(selected_machine)}
)



if not df.empty:
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])

    start_time = df["recorded_at"].min()
    end_time = df["recorded_at"].max()

    selected_start = st.selectbox(
        "Start Time",
        options=df["recorded_at"].tolist(),
        index=0,
        format_func=lambda t: t.strftime("%d/%m/%Y %H:%M")
    )

    selected_end = st.selectbox(
        "End Time",
        options=df["recorded_at"].tolist(),
        index=len(df) - 1,
        format_func=lambda t: t.strftime("%d/%m/%Y %H:%M")
    )

    df = df[
        (df["recorded_at"] >= selected_start) &
        (df["recorded_at"] <= selected_end)
    ].copy()
# ----------------------------------
# 4. Calculate monitoring summary
# ----------------------------------

total_readings = len(df)

anomaly_count = (
    df["predicted_status"] == "ANOMALY"
).sum()

latest_status = (
    df["predicted_status"].iloc[-1]
    if not df.empty
    else "NO DATA"
)

# ----------------------------------
# 5. Machine overview (KPIs)
# ----------------------------------

st.subheader("Machine Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Readings",
        total_readings
    )

with col2:
    st.metric(
        "Anomalies Detected",
        int(anomaly_count)
    )

with col3:
    st.metric(
        "Latest Status",
        latest_status
    )

# ----------------------------------
# 6. Sensor monitoring charts
# ----------------------------------

st.subheader("Sensor Monitoring")

if not df.empty:

    # Select anomaly records
    anomalies = df[
        df["predicted_status"] == "ANOMALY"
    ]

    # ------------------------------
    # Temperature chart
    # ------------------------------

    st.write("Temperature Monitoring")

    fig_temperature = go.Figure()

    fig_temperature.add_trace(go.Scatter(
        x=df["recorded_at"],
        y=df["temperature_c"],
        mode="lines+markers",
        name="Temperature"
    ))

    fig_temperature.add_trace(go.Scatter(
        x=anomalies["recorded_at"],
        y=anomalies["temperature_c"],
        mode="markers",
        marker=dict(
            color="red",
            size=12
        ),
        name="Anomaly"
    ))

    fig_temperature.update_layout(
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_temperature,
        use_container_width=True
    )

    # ------------------------------
    # Vibration chart
    # ------------------------------

    st.write("Vibration Monitoring")

    fig_vibration = go.Figure()

    fig_vibration.add_trace(go.Scatter(
        x=df["recorded_at"],
        y=df["vibration_mm_s"],
        mode="lines+markers",
        name="Vibration"
    ))

    fig_vibration.add_trace(go.Scatter(
        x=anomalies["recorded_at"],
        y=anomalies["vibration_mm_s"],
        mode="markers",
        marker=dict(
            color="red",
            size=12
        ),
        name="Anomaly"
    ))

    fig_vibration.update_layout(
        xaxis_title="Time",
        yaxis_title="Vibration (mm/s)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_vibration,
        use_container_width=True
    )

else:
    st.info("No sensor data available.")

st.subheader("Recent Anomaly Alerts")

if not df.empty:
    alerts = df[
        df["predicted_status"] == "ANOMALY"
    ].copy()

    alerts = alerts.sort_values(
        "recorded_at",
        ascending=False
    )

    if not alerts.empty:
        st.dataframe(
            alerts[[
                "recorded_at",
                "temperature_c",
                "vibration_mm_s",
                "predicted_status"
            ]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("No anomalies detected for this machine.")
else:
    st.info("No monitoring records available.")