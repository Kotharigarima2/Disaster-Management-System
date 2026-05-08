import pandas as pd
import time

from predict import predict_disaster
from priority_engine import calculate_priority, get_priority_level
from action_engine import get_action
from weather_service import get_weather_severity


def stream_tweets(file_path):

    df = pd.read_csv(file_path)

    print("\n--- Live Tweet Stream Started ---\n")

    tweets = []

    city = input("Enter city: ")
    weather_severity = get_weather_severity(city)

    print("Weather Severity:", weather_severity)
    print("-" * 50)

    for i, row in df.iterrows():

        tweet = row['text']
        tweets.append(tweet)

        # Predict disaster
        prediction = predict_disaster(tweet)

        print(f"\nTweet {i+1}: {tweet}")
        print("Prediction:", prediction)

        # Analyze current batch
        disaster_count = sum(1 for t in tweets if predict_disaster(t) == "Disaster")
        total = len(tweets)
        disaster_ratio = disaster_count / total

        # Calculate priority
        score = calculate_priority(disaster_count, disaster_ratio, weather_severity, tweets)
        priority = get_priority_level(score)
        actions = get_action(priority)

        print("\n--- LIVE STATUS ---")
        print("Total Tweets:", total)
        print("Disaster Tweets:", disaster_count)
        print("Priority:", priority)

        print("Actions:")
        for act in actions:
            print("-", act)

        print("-" * 50)

        time.sleep(2)  # delay for simulation