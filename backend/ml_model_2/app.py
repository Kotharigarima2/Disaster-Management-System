from flask import Flask, request, jsonify
from flask_cors import CORS

from predict import predict_disaster
from priority_engine import calculate_priority, get_priority_level
from weather_service import get_weather_severity
from action_engine import get_action
from news_service import fetch_disaster_news

app = Flask(__name__)
CORS(app)

@app.route("/live-news", methods=["GET"])
def live_news():

    headlines = fetch_disaster_news()

    if not headlines:
        return jsonify({"error": "No news fetched"}), 500

    tweets = headlines

    disaster_count = 0
    predictions = []

    for t in tweets:

        result = predict_disaster(t)

        predictions.append({
            "headline": t,
            "prediction": result
        })

        if result == "Disaster":
            disaster_count += 1

    total = len(tweets)
    disaster_ratio = disaster_count / total

    # Weather optional for live news
    weather_severity = 1

    score = calculate_priority(
        disaster_count,
        disaster_ratio,
        weather_severity,
        tweets
    )

    priority = get_priority_level(score)

    actions = get_action(priority)

    return jsonify({
        "total_news": total,
        "disaster_news": disaster_count,
        "priority": priority,
        "actions": actions,
        "news": predictions
    })
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json

    tweets = data.get("tweets", [])
    city = data.get("city", "")

    if not tweets:
        return jsonify({"error": "No tweets provided"}), 400

    # 🔥 Step 1: Predict tweets
    disaster_count = 0
    predictions = []

    for t in tweets:
        result = predict_disaster(t)
        predictions.append(result)

        if result == "Disaster":
            disaster_count += 1

    total = len(tweets)
    disaster_ratio = disaster_count / total

    # 🔥 Step 2: Weather
    weather_severity = get_weather_severity(city)

    # 🔥 Step 3: Priority
    score = calculate_priority(disaster_count, disaster_ratio, weather_severity, tweets)
    priority = get_priority_level(score)

    # 🔥 Step 4: Actions
    actions = get_action(priority)

    # 🔥 Response
    return jsonify({
        "total": total,
        "disaster_count": disaster_count,
        "ratio": round(disaster_ratio, 2),
        "weather": weather_severity,
        "priority": priority,
        "actions": actions,
        "predictions": predictions
    })


if __name__ == "__main__":
    app.run(debug=True)