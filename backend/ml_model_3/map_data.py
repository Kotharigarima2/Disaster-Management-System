import pandas as pd
from ml_model_3.predict import predict_disaster
from ml_model_3.locations import extract_locations

def generate_location_data(df):
    results = []

    for _, row in df.iterrows():
        tweet = row["text"]

        disaster = predict_disaster(tweet)
        locations = extract_locations(tweet)

        for loc in locations:
            results.append({
                "location": loc,
                "disaster": disaster,
                "tweet": tweet
            })

    return pd.DataFrame(results)