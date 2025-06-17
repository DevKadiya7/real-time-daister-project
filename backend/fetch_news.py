# backend/fetch_news.py
import requests

url = "https://newsapi.org/v2/everything?q=disaster OR earthquake OR flood&apiKey=YOUR_API_KEY"

response = requests.get(url)
data = response.json()

for article in data["articles"][:5]:
    print(article["title"], "➡", article["url"])
