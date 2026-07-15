from transformers import pipeline
import pandas as pd

# Load news data
df = pd.read_csv("data/ai_news.csv")

# Fake news detection model
classifier = pipeline(
    "text-classification",
    model="hamzab/roberta-fake-news-classification"
)

results = []

for title in df["title"]:
    prediction = classifier(str(title))[0]
    results.append(prediction["label"])

df["fake_news_prediction"] = results

# Save results
df.to_csv("data/news_with_fake_news.csv", index=False)

print(df[["title", "fake_news_prediction"]].head())
print("\nFake news detection completed!")