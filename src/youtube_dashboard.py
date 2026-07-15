import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from googleapiclient.discovery import build
from youtube_api_key import API_KEY


st.set_page_config(
    page_title="YouTube Sentiment Dashboard",
    layout="wide"
)

st.title("🎥 YouTube Sentiment Analysis Dashboard")
st.info("""
## 🤖 AI Powered YouTube Analytics

Analyze YouTube comments using Artificial Intelligence.

✔ Sentiment Analysis

✔ Interactive Charts

✔ Comment Filtering

✔ AI Insights

✔ CSV Export
""")
st.markdown("---")
# -----------------------------
# Connect to YouTube API
# -----------------------------
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

st.subheader("🔍 Search YouTube Videos")

search_query = st.text_input(
    "Enter Topic",
    placeholder="Example: Artificial Intelligence"
)

if st.button("Fetch Videos"):

    request = youtube.search().list(
        q=search_query,
        part="snippet",
        type="video",
        maxResults=10
    )

    response = request.execute()

    videos = []

    for item in response["items"]:

        print(item)

        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"]
        })

    videos_df = pd.DataFrame(videos)

    videos_df.to_csv(
        "data/youtube_videos.csv",
        index=False
    )

    st.success("✅ Videos fetched successfully!")

    st.dataframe(videos_df)

# Load saved videos
videos_df = pd.read_csv("data/youtube_videos.csv")

st.subheader("📺 Available Videos")
st.dataframe(videos_df)

selected_video = st.selectbox(
    "Select a Video",
    videos_df["title"].tolist()
)

selected_row = videos_df[
    videos_df["title"] == selected_video
].iloc[0]

st.write("### Selected Video")
st.write("📺", selected_row["title"])
st.write("📡 Channel:", selected_row["channel"])
st.write("🆔 Video ID:", selected_row["video_id"])
thumbnail_url = f"https://img.youtube.com/vi/{selected_row['video_id']}/0.jpg"

st.image(
    thumbnail_url,
    caption=selected_row["title"],
    width=400
)

if st.button("Fetch Comments"):

    with st.spinner("Fetching comments and analyzing sentiment..."):

        import subprocess
        import sys

        subprocess.run([
            sys.executable,
            "src/youtube_comments_multi.py"
        ])

        subprocess.run([
            sys.executable,
            "src/youtube_sentiment.py"
        ])

    st.success("✅ Comments fetched successfully!")


df = pd.read_csv("data/youtube_comments_sentiment.csv")

# Show only selected video's comments
if "selected_row" in locals():
    df = df[df["video_id"] == selected_row["video_id"]]

    if df.empty:
        st.warning("⚠️ No comments found for this video.")
        st.info("Possible reasons:")
        st.write("- Comments are disabled")
        st.write("- YouTube API didn't return comments")
        st.write("- Video has very few comments")
        st.stop()

st.write("Selected Video ID:", selected_row["video_id"])
st.write("Rows after filter:", len(df))
total_comments = len(df)
positive = len(df[df["sentiment"] == "Positive"])
neutral = len(df[df["sentiment"] == "Neutral"])
negative = len(df[df["sentiment"] == "Negative"])

st.markdown("---")
st.header("📊 Dashboard Overview")
st.caption("Real-time sentiment analysis of YouTube comments")
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="💬 Total Comments",
    value=total_comments
)

col2.metric(
    label="🟢 Positive",
    value=positive
)

col3.metric(
    label="⚪ Neutral",
    value=neutral
)

col4.metric(
    label="🔴 Negative",
    value=negative
)
st.subheader("📈 Sentiment Percentage")

positive_percent = (positive / total_comments) * 100
neutral_percent = (neutral / total_comments) * 100
negative_percent = (negative / total_comments) * 100

st.write(f"🟢 Positive: {positive_percent:.2f}%")
st.write(f"⚪ Neutral: {neutral_percent:.2f}%")
st.write(f"🔴 Negative: {negative_percent:.2f}%")
st.progress(positive_percent / 100)

st.progress(neutral_percent / 100)

st.progress(negative_percent / 100)
st.markdown("---")
st.subheader("🤖 AI Insights")

if positive_percent >= 70:
    st.success("""
### 😊 Overall Audience Reaction: Positive

✔ Most viewers liked the video.

✔ Audience appreciated the content quality.

✔ Very few negative comments were found.
""")

elif negative_percent >= 40:
    st.error("""
### 😟 Overall Audience Reaction: Negative

• Many users were dissatisfied.

• Video may need improvement.

• Negative comments dominate the discussion.
""")

else:
    st.info("""
### 😐 Overall Audience Reaction: Neutral

• Audience has mixed opinions.

• Positive and neutral comments are balanced.
""")

st.markdown("---")


col1, col2 = st.columns(2)

with col1:
   st.markdown("## 🥧 Sentiment Distribution")

sentiment_counts = df["sentiment"].value_counts()

fig, ax = plt.subplots(figsize=(5,5))

ax.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    shadow=True,
    explode=[0.05]*len(sentiment_counts)
)

ax.axis("equal")

st.pyplot(fig)


with col2:
    st.markdown("## 📊 Sentiment Count")

    st.bar_chart(sentiment_counts)
    st.markdown("---")
st.subheader("☁️ Most Frequent Words")

# Combine all comments into one text
text = " ".join(df["comment"].dropna().astype(str))

# Generate Word Cloud
wordcloud = WordCloud(
    width=900,
    height=400,
    background_color="white",
    colormap="viridis"
).generate(text)

# Display
fig, ax = plt.subplots(figsize=(12, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig)

st.markdown("---")

st.subheader("📈 Sentiment Percentage")

if total_comments > 0:
    positive_percent = (positive / total_comments) * 100
    neutral_percent = (neutral / total_comments) * 100
    negative_percent = (negative / total_comments) * 100
else:
    positive_percent = 0
    neutral_percent = 0
    negative_percent = 0
st.write(f"🟢 Positive: {positive_percent:.2f}%")
st.write(f"⚪ Neutral: {neutral_percent:.2f}%")
st.write(f"🔴 Negative: {negative_percent:.2f}%")
st.subheader("🔍 Filter Comments")

# Sentiment Filter
selected_sentiment = st.selectbox(
    "Select Sentiment",
    ["All", "Positive", "Neutral", "Negative"]
)

if selected_sentiment == "All":
    filtered_df = df
else:
    filtered_df = df[df["sentiment"] == selected_sentiment]

# Author Filter
authors = ["All"] + sorted(filtered_df["author"].dropna().unique().tolist())

selected_author = st.selectbox(
    "Select Author",
    authors
)

if selected_author != "All":
    filtered_df = filtered_df[
        filtered_df["author"] == selected_author
    ]
    st.subheader("🔎 Search Comments")

search = st.text_input("Enter a keyword")

if search:
    filtered_df = filtered_df[
        filtered_df["comment"].str.contains(search, case=False, na=False)
    ]
st.subheader("📊 Comments per Channel")

channel_summary = (
    df.groupby("channel")
      .size()
      .reset_index(name="Total Comments")
)

st.dataframe(channel_summary, use_container_width=True)

st.bar_chart(
    channel_summary.set_index("channel")
)

st.markdown("## 💬 YouTube Comments")

st.dataframe(
    filtered_df[
        [
            "video_id",
            "channel",
            "author",
            "comment",
            "likes",
            "published_at",
            "sentiment"
        ]
    ],
    use_container_width=True
)


csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv,
    file_name="youtube_comments_filtered.csv",
    mime="text/csv"
)
st.subheader("📊 Dataset Statistics")

st.write(df.describe(include="all"))


st.markdown("---")
st.success("✅ YouTube Sentiment Analysis Completed Successfully!")
st.markdown("---")

st.caption(
    "🚀 Developed by Swarna Mishra | Powered by Streamlit, YouTube API & Hugging Face Transformers"
)