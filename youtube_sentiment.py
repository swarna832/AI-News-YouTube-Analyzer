import pandas as pd
from transformers import pipeline

# Load comments
df = pd.read_csv("data/youtube_comments_multi.csv")

# Load sentiment analysis model
classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

# Map labels
label_map = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

sentiments = []

# Analyze each comment
for comment in df["comment"]:
    try:
        comment = str(comment)

        # Shorten very long comments
        if len(comment) > 300:
            comment = comment[:300]

        result = classifier(comment)[0]
        sentiments.append(label_map[result["label"]])

    except Exception as e:
        print(f"Skipped comment: {e}")
        sentiments.append("Neutral")

# Add sentiment column
df["sentiment"] = sentiments

# Save results
df.to_csv("data/youtube_comments_sentiment.csv", index=False)

print("✅ Sentiment Analysis Completed!")
print(df.head())