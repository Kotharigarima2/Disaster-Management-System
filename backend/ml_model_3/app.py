from flask import Flask, jsonify
from flask_cors import CORS

from load_data import load_data
from map_data import generate_location_data

app = Flask(__name__)
CORS(app)

@app.route("/disaster-data", methods=["GET"])
def get_data():
    train_df, dev_df, test_df = load_data()
    df = generate_location_data(test_df.head(200))
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(port=5003, debug=True)   # ✅ IMPORTANT