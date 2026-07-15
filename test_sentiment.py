from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

comments = [
    "This is the best video ever!",
    "I hate this video.",
    "This video is okay."
]

label_map = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

for comment in comments:
    result = classifier(comment)[0]
    print(comment)
    print("Raw Label:", result["label"])
    print("Mapped:", label_map[result["label"]])
    print("-" * 40)
    