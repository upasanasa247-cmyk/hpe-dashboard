import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
API_URL = "http://127.0.0.1:5000/devices"    

st.set_page_config(page_title="Network Monitoring Dashboard", layout="wide")

st.title(" Network Monitoring Dashboard")

# Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="datarefresh")

# ---------------- FETCH DATA ----------------
def load_data():
    try:
        response = requests.get(API_URL, timeout=5)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

data = load_data()

# Convert to DataFrame
df = pd.DataFrame(data)

# ---------------- CHECK IF DATA EXISTS ----------------
if df.empty:
    st.warning("No data available from API")
    st.stop()

# ---------------- CALCULATIONS ----------------
up_count = len(df[df["status"] == "UP"])
down_count = len(df[df["status"] == "DOWN"])

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Devices", len(df))
col2.metric("UP Devices", up_count)
col3.metric(" DOWN Devices", down_count)

st.divider()

# ---------------- PIE CHART ----------------
st.subheader("Device Status Distribution")

pie_fig = px.pie(
    names=["UP", "DOWN"],
    values=[up_count, down_count],
    color=["UP", "DOWN"],
    color_discrete_map={"UP": "green", "DOWN": "red"}
)

st.plotly_chart(pie_fig, use_container_width=True, key="pie_chart")

st.divider()

# ---------------- BAR CHART ----------------
st.subheader("Device Status Count")

bar_fig = px.bar(
    x=["UP", "DOWN"],
    y=[up_count, down_count],
    color=["UP", "DOWN"],
    color_discrete_map={"UP": "green", "DOWN": "red"}
)

st.plotly_chart(bar_fig, use_container_width=True, key="bar_chart")

st.divider()

# ---------------- TABLE ----------------
st.subheader("Device Details Table")

st.dataframe(df, use_container_width=True)

# ---------------- DOWN DEVICES ----------------
st.subheader(" Down Devices")

down_df = df[df["status"] == "DOWN"]

if not down_df.empty:
    st.dataframe(down_df, use_container_width=True)
else:
    st.success("All devices are UP ")