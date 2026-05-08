import pickle
from preprocessing import clean_text

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def keyword_override(text):
    keywords = [
        "earthquake", "flood", "explosion", "fire",
        "wildfire", "forest fire", "volcano", "eruption",
        "landslide", "collapse", "collapsed",
        "injured", "dead", "killed", "damage",
        "disaster", "emergency", "rescue"
    ]

    text = text.lower()
    return any(word in text for word in keywords)

def predict_disaster(text):
    if keyword_override(text):
        return "Disaster"
    
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned]).toarray()
    
    result = model.predict(vector)
    
    return "Disaster" if result[0] == 1 else "Not Disaster"