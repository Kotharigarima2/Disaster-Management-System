import os
import logging
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS

# =====================================================
# LOGGING CONFIG
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# =====================================================
# IMPORT ML MODELS
# =====================================================

# MODEL 1 → HUMAN NEED DETECTION
from ml_model.predict import predict

# MODEL 2 → DISASTER + PRIORITY ANALYSIS
from ml_model_2.predict import predict_disaster

from ml_model_2.priority_engine import (
    calculate_priority,
    get_priority_level
)

from ml_model_2.weather_service import (
    get_weather_severity
)

from ml_model_2.action_engine import (
    get_action
)

# MODEL 3 → MAP + LOCATION DATA
from ml_model_3.load_data import load_data
from ml_model_3.map_data import generate_location_data

# =====================================================
# LIVE NEWS FETCHER
# =====================================================

API_KEY = "2d04ecb3a2c44280832f5fce6ab3da47"


def fetch_live_news():

    print("\n========== FETCHING NEWS ==========\n")

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=disaster OR flood OR earthquake OR fire"
        f"&language=en"
        f"&sortBy=publishedAt"
        f"&apiKey={API_KEY}"
    )

    print("REQUEST URL:")
    print(url)

    response = requests.get(url)

    print("\nSTATUS CODE:")
    print(response.status_code)

    data = response.json()

    print("\nFULL API RESPONSE:")
    print(data)

    articles = []

    if "articles" in data:

        for article in data["articles"]:

            title = article.get("title", "")

            if title:
                articles.append(title)

    print("\nFETCHED ARTICLES:")
    print(articles)

    print("\n========== END ==========\n")

    return articles


# =====================================================
# HOME ROUTE
# =====================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "running",
        "message": "Disaster Management Backend API Live",
        "available_routes": {
            "health": "/health",
            "human_need_prediction": "/predict",
            "priority_analysis": "/analyze",
            "dashboard_data": "/disaster-data",
            "test_live": "/test-live",
            "live_analysis": "/live-analysis"
        }
    })


# =====================================================
# HEALTH CHECK ROUTE
# =====================================================

@app.route("/health", methods=["GET"])
def health_check():

    return jsonify({
        "success": True,
        "server": "active"
    }), 200


# =====================================================
# TEST ROUTE
# =====================================================

@app.route("/test-live")
def test_live():

    tweets = [
        "Massive flood situation near Yamuna river",
        "People trapped and need rescue",
        "Urgent medical supplies required",
        "Heavy rainfall destroying homes"
    ]

    final_results = []

    for tweet in tweets:

        disaster_result = predict_disaster(tweet)

        needs = predict(tweet)

        priority_score = calculate_priority(
            1,
            1,
            2,
            [tweet]
        )

        priority_level = get_priority_level(
            priority_score
        )

        final_results.append({
            "tweet": tweet,
            "disaster_prediction": disaster_result,
            "humanitarian_needs": needs,
            "priority_score": priority_score,
            "priority_level": priority_level
        })

    return jsonify({
        "success": True,
        "results": final_results
    })


# =====================================================
# LIVE ANALYSIS ROUTE
# =====================================================

@app.route("/live-analysis")
def live_analysis():

    try:

        tweets = fetch_live_news()

        final_results = []

        disaster_count = 0

        for tweet in tweets:

            logger.info(f"Incoming News: {tweet}")

            # Disaster Prediction
            disaster_result = predict_disaster(tweet)

            logger.info(
                f"Disaster Prediction: {disaster_result}"
            )

            if disaster_result == "Disaster":
                disaster_count += 1

            # Humanitarian Needs
            needs = predict(tweet)

            logger.info(
                f"Humanitarian Needs: {needs}"
            )

            final_results.append({
                "tweet": tweet,
                "disaster_prediction": disaster_result,
                "humanitarian_needs": needs
            })

        total = len(tweets)

        disaster_ratio = (
            disaster_count / total
            if total > 0 else 0
        )

        weather_severity = 2

        priority_score = calculate_priority(
            disaster_count,
            disaster_ratio,
            weather_severity,
            tweets
        )

        priority_level = get_priority_level(
            priority_score
        )

        logger.info(
            f"Priority Level: {priority_level}"
        )

        return jsonify({
            "success": True,

            "fetched_news": tweets,

            "total_news": total,

            "disaster_count": disaster_count,

            "priority_score": priority_score,

            "priority_level": priority_level,

            "results": final_results
        })

    except Exception as e:

        logger.error(
            f"Live Analysis Error: {str(e)}"
        )

        return jsonify({
            "success": False,
            "error": str(e)
        })


# =====================================================
# ROUTE 1 → HUMAN NEED DETECTION
# =====================================================

@app.route("/predict", methods=["POST"])
def predict_route():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        text = data.get("text", "").strip()

        if not text:

            return jsonify({
                "success": False,
                "error": "Text field is required"
            }), 400

        logger.info(
            f"Human Need Prediction Request: {text}"
        )

        needs = predict(text)

        return jsonify({
            "success": True,
            "input": text,
            "needs": needs
        }), 200

    except Exception as e:

        logger.error(
            f"Prediction Error: {str(e)}"
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =====================================================
# ROUTE 2 → DISASTER PRIORITY ANALYSIS
# =====================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        tweets = data.get("tweets", [])
        city = data.get("city", "Unknown")

        if not tweets or not isinstance(tweets, list):

            return jsonify({
                "success": False,
                "error": "Tweets list is required"
            }), 400

        disaster_count = 0

        predictions = []

        for tweet in tweets:

            result = predict_disaster(tweet)

            predictions.append({
                "tweet": tweet,
                "prediction": result
            })

            if result == "Disaster":
                disaster_count += 1

        total = len(tweets)

        disaster_ratio = (
            disaster_count / total
            if total > 0 else 0
        )

        weather_severity = get_weather_severity(
            city
        )

        score = calculate_priority(
            disaster_count,
            disaster_ratio,
            weather_severity,
            tweets
        )

        priority = get_priority_level(score)

        actions = get_action(priority)

        response = {
            "success": True,
            "city": city,
            "total_tweets": total,
            "disaster_count": disaster_count,
            "disaster_ratio": round(
                disaster_ratio,
                2
            ),
            "weather_severity": weather_severity,
            "priority_score": score,
            "priority_level": priority,
            "recommended_actions": actions,
            "tweet_predictions": predictions
        }

        logger.info(
            f"Priority Analysis Completed for {city}"
        )

        return jsonify(response), 200

    except Exception as e:

        logger.error(
            f"Analyze Error: {str(e)}"
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =====================================================
# ROUTE 3 → LIVE DASHBOARD DATA
# =====================================================

@app.route("/disaster-data", methods=["GET"])
def get_disaster_data():

    try:

        train_df, dev_df, test_df = load_data()

        generated_df = generate_location_data(
            test_df.head(200)
        )

        return jsonify({
            "success": True,
            "count": len(generated_df),
            "data": generated_df.to_dict(
                orient="records"
            )
        }), 200

    except Exception as e:

        logger.error(
            f"Dashboard Data Error: {str(e)}"
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =====================================================
# GLOBAL ERROR HANDLER
# =====================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "error": "Route not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):

    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# =====================================================
# MAIN ENTRY
# =====================================================

if __name__ == "__main__":

    PORT = int(
        os.environ.get("PORT", 5001)
    )

    logger.info(
        f"Starting server on port {PORT}"
    )

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True
    )