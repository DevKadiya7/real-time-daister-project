from flask import Flask, jsonify
from fetch_news import get_news

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route("/")
def index():
    return "Welcome to the Disaster News API. Use /api/disasters to get data." 


@app.route("/api/disasters")
def get_disasters():
    news_data = get_news()
    return jsonify(news_data)

if __name__ == "__main__":
    app.run(debug=True)
