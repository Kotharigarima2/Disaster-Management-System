from flask import Flask, request, jsonify
from flask_cors import CORS

# =====================================================
# IMPORTS
# =====================================================

# ML MODEL 1
from ml_model.predict import predict

# ML MODEL 2
from ml_model_2.predict import predict_disaster
from ml_model_2.priority_engine import (
    calculate_priority,
    get_priority_level
)
from ml_model_2.weather_service import (
    get_weather_severity
)
from ml_model_2.action_engine import get_action

# ML MODEL 3
from ml_model_3.load_data import load_data
from ml_model_3.map_data import generate_location_data


# =====================================================
# APP
# =====================================================

app = Flask(__name__)
CORS(app)


# =====================================================
# ROUTE 1 → HUMAN NEEDS
# =====================================================

@app.route("/predict", methods=["POST"])
def predict_route():

    try:

        data = request.get_json()

        text = data.get("text", "")

        needs = predict(text)

        return jsonify({
            "needs": needs
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =====================================================
# ROUTE 2 → PRIORITY ANALYSIS
# =====================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.json

        tweets = data.get("tweets", [])
        city = data.get("city", "")

        if not tweets:
            return jsonify({
                "error": "No tweets provided"
            }), 400

        disaster_count = 0
        predictions = []

        for t in tweets:

            result = predict_disaster(t)

            predictions.append(result)

            if result == "Disaster":
                disaster_count += 1

        total = len(tweets)

        disaster_ratio = disaster_count / total

        weather_severity = get_weather_severity(city)

        score = calculate_priority(
            disaster_count,
            disaster_ratio,
            weather_severity,
            tweets
        )

        priority = get_priority_level(score)

        actions = get_action(priority)

        return jsonify({
            "total": total,
            "disaster_count": disaster_count,
            "ratio": round(disaster_ratio, 2),
            "weather": weather_severity,
            "priority": priority,
            "actions": actions,
            "predictions": predictions
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =====================================================
# ROUTE 3 → DASHBOARD DATA
# =====================================================

@app.route("/disaster-data", methods=["GET"])
def get_data():

    try:

        train_df, dev_df, test_df = load_data()

        df = generate_location_data(
            test_df.head(200)
        )

        return jsonify(
            df.to_dict(orient="records")
        )

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    app.run(port=5001, debug=True)