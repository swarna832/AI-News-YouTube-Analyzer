import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

df = pd.read_csv("data/ai_news.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chromadb_data")

collection = client.get_or_create_collection(
    name="news_embeddings"
)

for i, row in df.iterrows():

    title = str(row["title"])

    embedding = model.encode(title).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[title]
    )

print("Embeddings stored successfully!")
print("Total records:", collection.count())