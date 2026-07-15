import streamlit as st
import pandas as pd

st.title("📰 AI Sentiment Analysis & Fake News Detection")

st.write("""
This dashboard analyzes news articles using AI models.

It performs:
- Sentiment Analysis
- Fake News Detection
- News Data Visualization
""")

# Load datasets
sentiment_df = pd.read_csv("data/news_with_sentiment.csv")
fake_df = pd.read_csv("data/news_with_fake_news.csv")

# Convert sentiment labels
sentiment_df["sentiment"] = sentiment_df["sentiment"].replace({
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
})

final_df = sentiment_df.copy()

if "fake_news_prediction" in fake_df.columns:
    final_df["fake_news_prediction"] = fake_df["fake_news_prediction"]

# -----------------------------
# Sentiment Statistics
# -----------------------------
st.subheader("📊 Sentiment Statistics")
# -----------------------------
# Dashboard Metrics
# -----------------------------
total_news = len(final_df)

positive = len(final_df[final_df["sentiment"] == "Positive"])
neutral = len(final_df[final_df["sentiment"] == "Neutral"])
negative = len(final_df[final_df["sentiment"] == "Negative"])

fake_news = len(
    final_df[
        final_df["fake_news_prediction"]
        .astype(str)
        .str.contains("fake", case=False, na=False)
    ]
)

st.markdown("---")
st.header("📊 News Dashboard Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📰 Total News", total_news)
col2.metric("🟢 Positive", positive)
col3.metric("⚪ Neutral", neutral)
col4.metric("🔴 Negative", negative)
col5.metric("🚨 Fake News", fake_news)
st.bar_chart(
    final_df["sentiment"].value_counts()
)
st.markdown("---")

st.subheader("🥧 Sentiment Distribution")

sentiment_counts = final_df["sentiment"].value_counts()

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5, 5))

ax.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    shadow=True,
    explode=[0.05] * len(sentiment_counts)
)

ax.axis("equal")

st.pyplot(fig)
st.markdown("---")

st.subheader("🤖 AI Insights")

positive_percent = (positive / total_news) * 100
negative_percent = (negative / total_news) * 100
fake_percent = (fake_news / total_news) * 100

if positive_percent >= 60:
    st.success(f"""
### 😊 Overall News Sentiment: Positive

✅ {positive_percent:.1f}% of the news articles have a Positive sentiment.

🚨 Fake News detected: {fake_percent:.1f}%

Overall, the news dataset appears reliable and mostly positive.
""")

elif negative_percent >= 40:
    st.error(f"""
### 😟 Overall News Sentiment: Negative

⚠️ {negative_percent:.1f}% of the news articles have a Negative sentiment.

🚨 Fake News detected: {fake_percent:.1f}%

The dataset contains a significant amount of negative news.
""")

else:
    st.info(f"""
### 😐 Overall News Sentiment: Neutral

Positive: {positive_percent:.1f}%

Negative: {negative_percent:.1f}%

Fake News: {fake_percent:.1f}%

The overall sentiment is balanced.
""")

# -----------------------------
# Search News
# -----------------------------
search = st.text_input("🔍 Search News")

if search:
    final_df = final_df[
        final_df["title"].str.contains(search, case=False, na=False)
    ]

# -----------------------------
# News Results
# -----------------------------
st.markdown("---")
st.subheader("🔍 Filter News")

sentiment_filter = st.selectbox(
    "Select Sentiment",
    ["All", "Positive", "Neutral", "Negative"]
)

fake_filter = st.selectbox(
    "Fake News",
    ["All", "Fake", "Real"]
)

filtered_df = final_df.copy()

# Sentiment Filter
if sentiment_filter != "All":
    filtered_df = filtered_df[
        filtered_df["sentiment"] == sentiment_filter
    ]

# Fake News Filter
if fake_filter == "Fake":
    filtered_df = filtered_df[
        filtered_df["fake_news_prediction"]
        .astype(str)
        .str.contains("fake", case=False, na=False)
    ]

elif fake_filter == "Real":
    filtered_df = filtered_df[
        ~filtered_df["fake_news_prediction"]
        .astype(str)
        .str.contains("fake", case=False, na=False)
    ]
st.subheader("📰 News Analysis Results")

st.dataframe(
    filtered_df[
        [
            "title",
            "sentiment",
            "fake_news_prediction"
        ]
    ],
    use_container_width=True
)
st.markdown("---")

st.subheader("📥 Download News Analysis")

csv = final_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download News CSV",
    data=csv,
    file_name="news_analysis.csv",
    mime="text/csv"
)
st.success("✅ Analysis Completed Successfully!")