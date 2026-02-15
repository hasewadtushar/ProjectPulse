import sys
import os

# ✅ FIX MODULE PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import re
import plotly.express as px
import plotly.graph_objects as go
from data_processing.channel_extractor import extract_channel_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

# ---------------- CUSTOM CARD CSS ----------------
st.markdown("""
<style>
.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    text-align: center;
}
.title {
    text-align: center;
}
.description {
    text-align: center;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1 class='title'>📊 YouTube Creator Analytics Dashboard</h1>", unsafe_allow_html=True)

st.markdown("""
<p class='description'>
This dashboard allows users to enter a valid YouTube Channel ID and fetch
real-time channel statistics including subscriber count, total videos, and total views.
</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
channel_id = st.text_input(
    "🔎 Enter YouTube Channel ID (Must start with UC...)",
    placeholder="Example: UCxxxxxxxxxxxxxxxxxxxxxx"
)

submit = st.button("🚀 Fetch Channel Data")

# ---------------- VALIDATION FUNCTION ----------------
def is_valid_channel_id(cid):
    pattern = r"^UC[a-zA-Z0-9_-]{22}$"
    return re.match(pattern, cid)

# ---------------- MAIN ----------------
if submit:

    if not channel_id:
        st.error("⚠ Please enter a Channel ID.")
        st.stop()

    if not is_valid_channel_id(channel_id):
        st.error("❌ Invalid Channel ID format. It must start with 'UC' and be 24 characters long.")
        st.stop()

    # Fetch Data
    with st.spinner("Fetching channel data from YouTube API... ⏳"):
        data_df = extract_channel_data(channel_id)

    # DataFrame Check
    if data_df is None or data_df.empty:
        st.error("❌ Channel not found. Please check the ID.")
        st.stop()

    data = data_df.iloc[0]

    # ---------------- DISPLAY ----------------
    st.success("Channel Loaded Successfully ✅")

    st.markdown("### 📌 Channel Overview")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
        <div class="card">
            <h3>👥 Subscribers</h3>
            <h2>{data['subscriber_count']:,}</h2>
        </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
        <div class="card">
            <h3>🎬 Total Videos</h3>
            <h2>{data['total_videos']:,}</h2>
        </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
        <div class="card">
            <h3>👁 Total Views</h3>
            <h2>{data['total_views']:,}</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### 📺 Channel Name: {data['channel_name']}")

    # ---------------- INTERACTIVE ANALYTICS ----------------
    st.markdown("## 📊 Interactive Analytics Dashboard")

    # Prepare data for charts
    metrics_df = data_df[['subscriber_count', 'total_videos', 'total_views']].copy()

    metrics_df = metrics_df.rename(columns={
        'subscriber_count': 'Subscribers',
        'total_videos': 'Total Videos',
        'total_views': 'Total Views'
    })

    plot_df = metrics_df.melt(var_name="Metric", value_name="Value")

    # ---------------- BAR CHART ----------------
    fig_bar = px.bar(
        plot_df,
        x="Metric",
        y="Value",
        color="Metric",
        text="Value",
        title="Channel Statistics Overview",
    )

    fig_bar.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_bar.update_layout(
        xaxis_title="Metrics",
        yaxis_title="Count",
        showlegend=False
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # ---------------- PIE CHART ----------------
    fig_pie = px.pie(
        plot_df,
        names="Metric",
        values="Value",
        title="Distribution of Channel Metrics"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # ---------------- DONUT CHART ----------------
    fig_donut = go.Figure(data=[go.Pie(
        labels=plot_df["Metric"],
        values=plot_df["Value"],
        hole=0.5
    )])

    fig_donut.update_layout(title_text="Channel Metrics (Donut View)")

    st.plotly_chart(fig_donut, use_container_width=True)




from data_processing.video_extractor import extract_all_videos_from_channel

st.markdown("---")
st.markdown("## 🎬 Channel Videos")

if st.button("📥 Load All Videos"):

    with st.spinner("Fetching all videos... This may take time ⏳"):
        video_df = extract_all_videos_from_channel(channel_id)

    if video_df.empty:
        st.warning("No videos found.")
    else:
        st.success(f"Fetched {len(video_df)} videos successfully!")

        # Show dataframe in UI
        st.dataframe(video_df)

        # Optional: Show Top 5 Videos by Views
        st.markdown("###  Top 5 Videos by Views")

        top_videos = video_df.sort_values(by="view_count", ascending=False).head(5)

        st.dataframe(top_videos[["title", "view_count"]])
