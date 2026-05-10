from flask import Flask, jsonify
from flask_cors import CORS

from news_fetcher import fetch_disaster_news
from predictor import predict_all

app = Flask(__name__)
CORS(app)

@app.route("/news-needs", methods=["GET"])
def get_news():

    news = fetch_disaster_news()

    results = []

    for item in news:

        # safety check (API sometimes returns None)
        if not item:
            continue

        result = predict_all(item)

        results.append({
            "text": item,
            "disaster": result.get("disaster"),
            "type": result.get("type"),
            "needs": result.get("needs", []),
            "priority": result.get("priority")
        })

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5001, debug=True)