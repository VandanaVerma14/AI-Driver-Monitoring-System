import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.express as px

st.set_page_config(
    page_title="AI Driver Monitoring Dashboard",
    page_icon="🚗",
    layout="wide",
)

st.caption(
    "Real-Time Driver Fatigue & Distraction Analytics"
)
# -----------------------------
# Load Database
# -----------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "driver_monitor.db"

connection = sqlite3.connect(DB_PATH)

# -----------------------------
# Find Latest Trip
# -----------------------------

latest_trip = pd.read_sql_query(
    "SELECT MAX(trip_id) AS trip FROM events",
    connection,
)

# If database has no trips
if latest_trip.iloc[0]["trip"] is None:

    st.warning("No trip data found.")

    st.stop()

current_trip = int(latest_trip.iloc[0]["trip"])

# Temporary Debug (we'll remove later)
st.write("Latest Trip:", current_trip)

# -----------------------------
# Load Only Current Trip
# -----------------------------

df = pd.read_sql_query(
    """
    SELECT *
    FROM events
    WHERE trip_id = ?
    ORDER BY id DESC
    """,
    connection,
    params=[current_trip],
)

# Temporary Debug (we'll remove later)
st.write(df.head())

connection.close()

# -----------------------------
# If Database Empty
# -----------------------------

if df.empty:

    st.warning("No trip data found.")

    st.stop()

# -----------------------------
# Statistics
# -----------------------------

blink_count = (df["event"] == "Blink").sum()

yawn_count = (df["event"] == "Yawn").sum()

microsleep_count = (df["event"] == "Microsleep").sum()

direction_changes = (df["event"] == "Direction").sum()

# -----------------------------
# Dashboard Cards
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👁 Blinks",
    blink_count,
)

col2.metric(
    "😮 Yawns",
    yawn_count,
)

col3.metric(
    "😴 Microsleeps",
    microsleep_count,
)

col4.metric(
    "🚘 Direction Changes",
    direction_changes,
)

st.divider()

# -----------------------------
# Event Table
# -----------------------------
#########################################
# Dashboard Layout
#########################################

left, right = st.columns(2)
with left:

    st.subheader("📊 Event Distribution")

    event_counts = (
        df["event"]
        .value_counts()
        .reset_index()
    )

    event_counts.columns = [
        "Event",
        "Count",
    ]

    fig = px.pie(
        event_counts,
        names="Event",
        values="Count",
        hole=0.4,
        title="Driver Events",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
with right:

    st.subheader("📈 Event Timeline")

    timeline_df = df.copy()

    timeline_df["timestamp"] = pd.to_datetime(
        timeline_df["timestamp"]
    )

    fig = px.scatter(
        timeline_df,
        x="timestamp",
        y="event",
        color="event",
        title="Event Timeline",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )
st.divider()

st.subheader("📋 Recent Events")
st.dataframe(
    df.head(20),
    use_container_width=True,
    hide_index=True,
)