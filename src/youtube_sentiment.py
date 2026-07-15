from transformers import pipeline
import pandas as pd

df = pd.read_csv("data/youtube_comments_multi.csv")


classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)


def map_sentiment(label):
    if label == "LABEL_0":
        return "Negative"
    elif label == "LABEL_1":
        return "Neutral"
    elif label == "LABEL_2":
        return "Positive"
    else:
        return "Unknown"


sentiments = []

# Analyze each comment
for comment in df["comment"]:
    result = classifier(str(comment))[0]
    sentiments.append(map_sentiment(result["label"]))

# Add sentiment column
df["sentiment"] = sentiments

# Save results
df.to_csv("data/youtube_comments_sentiment.csv", index=False)

print("Sentiment analysis completed successfully!")

print("\nSentiment Distribution:")
print(df["sentiment"].value_counts())