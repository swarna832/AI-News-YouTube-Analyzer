from googleapiclient.discovery import build
import pandas as pd
from youtube_api_key import API_KEY

youtube = build("youtube", "v3", developerKey=API_KEY)


VIDEO_ID = "ad79nYk2keg"


request = youtube.commentThreads().list(
    part="snippet",
    videoId=VIDEO_ID,
    maxResults=50,
    textFormat="plainText"
)

response = request.execute()

comments = []

for item in response["items"]:
    comment = item["snippet"]["topLevelComment"]["snippet"]

    comments.append({
    "video_id": video_id,
    "author": author,
    "comment": comment,
    "likes": likes,
    "published_at": published_at
})

df = pd.DataFrame(comments)

df.to_csv("data/youtube_comments.csv", index=False)

print("Comments saved successfully!")
print(df.head())