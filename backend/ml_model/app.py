from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict  

app = Flask(__name__)
CORS(app)  

@app.route("/predict", methods=["POST"])
def predict_route():
    try:
        data = request.get_json()
        text = data.get("text", "")
        needs = predict(text)  
        return jsonify({"needs": needs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)