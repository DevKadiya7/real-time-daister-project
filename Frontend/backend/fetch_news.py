import requests

API_KEY = "7800ff24f230406098c8b746e87e7296"
URL = f"https://newsapi.org/v2/everything?q=disaster OR earthquake OR flood&sortBy=publishedAt&language=en&apiKey={API_KEY}"

def get_news():
    response = requests.get(URL)
    data = response.json()

    articles = []
    for article in data.get("articles", [])[:10]:
        articles.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "image": article.get("urlToImage", None)
        })
    return articles


