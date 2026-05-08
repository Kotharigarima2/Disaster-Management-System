import pickle
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(BASE_DIR, "models")

model = pickle.load(open(os.path.join(model_dir, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(model_dir, "vectorizer.pkl"), "rb"))

def predict_disaster(text):
    text_vec = vectorizer.transform([text])
    return model.predict(text_vec)[0]