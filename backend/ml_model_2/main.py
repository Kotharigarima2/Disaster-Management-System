from predict import predict_disaster
from priority_engine import calculate_priority, get_priority_level
from weather_service import get_weather_severity
from action_engine import get_action
from tweet_stream import stream_tweets


def simulate_system():
    tweets = []

    print("\nEnter tweets (type 'done' to stop):")

    while True:
        text = input("Tweet: ")

        if text.lower() == "done":
            break

        tweets.append(text)

    if len(tweets) == 0:
        print("No data")
        return

    # Analyze tweets
    disaster_count = 0

    for t in tweets:
        if predict_disaster(t) == "Disaster":
            disaster_count += 1

    total = len(tweets)
    disaster_ratio = disaster_count / total

    # Weather
    city = input("Enter city: ")
    weather_severity = get_weather_severity(city)

    # Priority
    score = calculate_priority(disaster_count, disaster_ratio, weather_severity, tweets)
    priority = get_priority_level(score)

    # Actions
    actions = get_action(priority)

    # Debug info
    print("\n--- DEBUG INFO ---")
    print("Total Tweets:", total)
    print("Disaster Tweets:", disaster_count)
    print("Disaster Ratio:", round(disaster_ratio, 2))
    print("Weather Severity:", weather_severity)

    # Final output
    print("\n--- RESULT ---")
    print("Priority Level:", priority)

    print("\nRecommended Actions:")
    for act in actions:
        print("-", act)


# 🔥 MAIN CONTROL
if __name__ == "__main__":

    print("1. Manual Input")
    print("2. Live Tweet Stream")

    choice = input("Choose option: ")

    if choice == "1":
        simulate_system()

    elif choice == "2":
        stream_tweets("data/final_dataset.csv")

    else:
        print("Invalid choice")