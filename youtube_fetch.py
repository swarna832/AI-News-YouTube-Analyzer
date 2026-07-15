from googleapiclient.discovery import build
import pandas as pd
from youtube_api_key import API_KEY

# Connect to YouTube API
youtube = build("youtube", "v3", developerKey=API_KEY)

# Search for videos
request = youtube.search().list(
    q="Artificial Intelligence",
    part="snippet",
    type="video",
    maxResults=10
)

response = request.execute()

videos = []

# Extract required information
for item in response["items"]:
    video = {
        "video_id": item["id"].get("videoId", ""),
        "title": item["snippet"].get("title", ""),
        "channel": item["snippet"].get("channelTitle", ""),
        "published_at": item["snippet"].get("publishedAt", "")
    }

    print(video)      # <-- This will print each video in the terminal
    videos.append(video)

# Create DataFrame
df = pd.DataFrame(videos)

print("\nColumns in DataFrame:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

# Save CSV
df.to_csv("data/youtube_videos.csv", index=False)

print("\nYouTube videos saved successfully!")