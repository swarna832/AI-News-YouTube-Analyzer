import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts")

data = response.json()

print("Total Posts:", len(data))
print("\nFirst Post:\n")
print(data[0]["title"])