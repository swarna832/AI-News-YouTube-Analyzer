from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

text = "Artificial Intelligence is transforming healthcare."

embedding = model.encode(text)

print("Embedding Length:", len(embedding))
print("First 10 values:")
print(embedding[:10])