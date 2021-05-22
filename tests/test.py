import requests

BASE = "http://127.0.0.1:5000/api/posts"

response = requests.get(BASE + "?tags=science,tech&sortBy=id&direction=desc")

print(response.json())
