import os
import pickle
from .locations import extract_locations

BASE_DIR = os.path.dirname(__file__)

model_path = os.path.join(BASE_DIR, "models", "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))
# Predict function
def predict_disaster(text):

    text_vec = vectorizer.transform([text])

    prediction = model.predict(text_vec)[0]

    return prediction


# Manual testing
if __name__ == "__main__":

    while True:

        tweet = input("\nEnter a tweet (or type exit): ")

        if tweet.lower() == "exit":
            break

        disaster = predict_disaster(tweet)

        locations = extract_locations(tweet)

        print("\n===== RESULT =====")
        print("Tweet:", tweet)
        print("Disaster:", disaster)
        print("Location(s):", locations)