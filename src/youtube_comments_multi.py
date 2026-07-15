 import sys
from googleapiclient.discovery import build
import pandas as pd
from youtube_api_key import API_KEY

youtube = build("youtube", "v3", developerKey=API_KEY)
if len(sys.argv) > 1:
    video_id = sys.argv[1]
    videos = pd.DataFrame([{
        "video_id": video_id,
        "channel": "Selected Channel"
    }])
else:
    videos = pd.read_csv("data/youtube_videos.csv")

all_comments = []

for _, row in videos.iterrows():

    video_id = row["video_id"]
    channel = row["channel"]

    print(f"Fetching comments for Video ID: {video_id}")

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20,
            textFormat="plainText"
        )

        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]

            all_comments.append({
                "video_id": video_id,
                "channel": channel,
                "author": comment["authorDisplayName"],
                "comment": comment["textDisplay"],
                "likes": comment["likeCount"],
                "published_at": comment["publishedAt"]
            })

    except Exception as e:
        print(f"Skipped {video_id}: {e}")
        # Convert comments to DataFrame
df = pd.DataFrame(all_comments)

# Save to CSV
df.to_csv("data/youtube_comments_multi.csv", index=False)

print("✅ Comments saved successfully!")
print(df.head())
