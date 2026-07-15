from transformers import pipeline
import pandas as pd

df = pd.read_csv("data/ai_news.csv")

# Sentiment model
classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

sentiments = []

for title in df["title"]:
    result = classifier(str(title))[0]
    sentiments.append(result["label"])

df["sentiment"] = sentiments

# Save results
df.to_csv("data/news_with_sentiment.csv", index=False)

print(df[["title", "sentiment"]].head())
print("\nSentiment analysis completed!")