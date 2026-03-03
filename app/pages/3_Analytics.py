import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.styling import apply_custom_styles
from utils.session import initialize_session_state

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
apply_custom_styles()
initialize_session_state()

# Title
st.title("📊 Research Analytics Dashboard")
st.write("Visual insights into your academic collection and system usage.")

# Data Preparation
papers_df = pd.DataFrame(st.session_state.papers)
if papers_df.empty:
    st.warning("No papers found to analyze.")
    st.stop()

# Ensure numeric year
papers_df["year"] = pd.to_numeric(papers_df["year"], errors='coerce').fillna(2024).astype(int)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    # Papers by Year
    st.subheader("📅 Temporal Distribution")
    year_dist = papers_df.groupby("year").size().reset_index(name="count")
    fig_year = px.bar(year_dist, x="year", y="count", 
                      title="Papers by Publication Year", 
                      color_discrete_sequence=['#6366F1'])
    fig_year.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_year, use_container_width=True)

with col2:
    # Topic Distribution
    st.subheader("🧬 Thematic Distribution")
    topic_dist = papers_df.groupby("topic").size().reset_index(name="count")
    fig_topic = px.pie(topic_dist, values="count", names="topic", 
                      title="Distribution of Research Topics",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_topic.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_topic, use_container_width=True)

st.markdown("---")

# Usage Statistics
st.subheader("🛠️ System Usage & Performance")
u_col1, u_col2, u_col3 = st.columns(3)

with u_col1:
    total_tokens = st.session_state.token_usage.get("total_tokens", 0)
    st.metric(label="Total Tokens Used", value=f"{total_tokens:,}", delta=f"{total_tokens//1000}k", delta_color="normal")
    st.caption("Aggregated across all sessions")

with u_col2:
    avg_latency = np.mean(st.session_state.latency) if st.session_state.latency else 0
    st.metric(label="Avg Retrieval Latency", value=f"{avg_latency:.2f}s", delta=f"{avg_latency-1.5:.2f}s", delta_color="inverse")
    st.caption("Based on last 10 queries")

with u_col3:
    query_count = len(st.session_state.messages) // 2
    st.metric(label="Total Queries", value=query_count, delta=query_count, delta_color="normal")
    st.caption("Current session count")

st.markdown("---")

# Latency Trend
st.subheader("📈 Performance Trend (Latency)")
latency_df = pd.DataFrame({"Query": range(len(st.session_state.latency)), "Latency (s)": st.session_state.latency})
fig_latency = px.area(latency_df, x="Query", y="Latency (s)", 
                     title="System Response Time over Time",
                     color_discrete_sequence=['#8B5CF6'])
fig_latency.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
# Fixed axis name
fig_latency.update_xaxes(title="Recent Queries")
st.plotly_chart(fig_latency, use_container_width=True)

# Data Table
st.subheader("📄 Raw Collection Data")
st.dataframe(papers_df[["title", "author", "year", "topic"]], use_container_width=True)
