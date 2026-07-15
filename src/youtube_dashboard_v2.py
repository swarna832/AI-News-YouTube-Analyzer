import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from youtube_api_key import API_KEY

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="YouTube Dashboard V2",
    layout="wide"
)

st.title("🎥 YouTube Video Explorer")

# -----------------------------
# YouTube API
# -----------------------------
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

# -----------------------------
# Search Topic
# -----------------------------
search_query = st.text_input(
    "Enter Topic",
    placeholder="Example: Artificial Intelligence"
)

# -----------------------------
# Fetch Videos
# -----------------------------
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

        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"]
        })

    videos_df = pd.DataFrame(videos)

    # Save for future steps
    videos_df.to_csv(
        "data/youtube_videos.csv",
        index=False
    )

    st.success("✅ Videos fetched successfully!")

# -----------------------------
# Show Videos
# -----------------------------
try:

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

    st.markdown("### Selected Video")

    st.write("📺 Title :", selected_row["title"])
    st.write("📡 Channel :", selected_row["channel"])
    st.write("🆔 Video ID :", selected_row["video_id"])

except:
    st.info("Search a topic and click 'Fetch Videos'.")