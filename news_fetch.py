from newsapi import NewsApiClient
import pandas as pd

# Enter your API key here
api_key = "7df8938542ba45fca71249b25dfe1a60"
newsapi = NewsApiClient(api_key=api_key)

articles = newsapi.get_everything(
    q="Artificial Intelligence",
    language="en",
    sort_by="publishedAt",
    page_size=10
)

data = []

for article in articles["articles"]:
    data.append({
        "title": article["title"],
        "source": article["source"]["name"],
        "published": article["publishedAt"]
    })

df = pd.DataFrame(data)

df.to_csv("data/ai_news.csv", index=False)

print("News articles saved successfully!")
print(df.head())