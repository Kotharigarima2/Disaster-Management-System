import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from load_data import load_data

# Base dir = backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model folder
model_dir = os.path.join(BASE_DIR, "models")
os.makedirs(model_dir, exist_ok=True)

# Load data
train_df, dev_df, test_df = load_data()

X_train = train_df["text"]
y_train = train_df["label"]

# Vectorizer
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)

# Model
model = LogisticRegression(max_iter=200)
model.fit(X_train_vec, y_train)

# Save
pickle.dump(model, open(os.path.join(model_dir, "model.pkl"), "wb"))
pickle.dump(vectorizer, open(os.path.join(model_dir, "vectorizer.pkl"), "wb"))

print("✅ Model trained and saved successfully.")