import json
import pandas as pd
import re
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

os.makedirs("model", exist_ok=True)

# =========================
# 🔹 Load JSON
# =========================
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))

train = load_json("data/train.json")
test = load_json("data/test.json")

# =========================
# 🔹 Clean Text
# =========================
def clean(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

train["clean"] = train["text"].apply(clean)
test["clean"] = test["text"].apply(clean)

# =========================
# 🔹 Disaster Type Label
# =========================
def get_type(event):
    event = str(event).lower()
    if "earthquake" in event: return "earthquake"
    if "flood" in event: return "flood"
    if "cyclone" in event or "hurricane" in event: return "cyclone"
    if "tornado" in event: return "tornado"
    if "explosion" in event: return "explosion"
    return "other"

train["type"] = train["event"].apply(get_type)
test["type"] = test["event"].apply(get_type)

# =========================
# 🔹 Vectorizer
# =========================
vectorizer = TfidfVectorizer(max_features=8000, ngram_range=(1,2))

X_train = vectorizer.fit_transform(train["clean"])
X_test = vectorizer.transform(test["clean"])

# =========================
# 🔹 Model 1: Needs
# =========================
need_model = LogisticRegression(max_iter=500)
need_model.fit(X_train, train["class_label"])

print("Need accuracy:", need_model.score(X_test, test["class_label"]))

# =========================
# 🔹 Model 2: Disaster Type
# =========================
type_model = LogisticRegression(max_iter=500)
type_model.fit(X_train, train["type"])

print("Type accuracy:", type_model.score(X_test, test["type"]))

# =========================
# 🔹 SAVE MODELS (FIXED PATHS)
# =========================
joblib.dump(need_model, "model/need_model.pkl")
joblib.dump(type_model, "model/type_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("✅ Models saved correctly")