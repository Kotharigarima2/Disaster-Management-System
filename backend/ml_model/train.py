import pandas as pd
import re
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# =========================
# 🔹 Load Dataset
# =========================
train = pd.read_csv("data/humaid_train.csv")
test = pd.read_csv("data/humaid_test.csv")

# =========================
# 🔹 Clean Text
# =========================
def clean_text(text):
    text = str(text).lower()

    slang_dict = {
        "plz": "please",
        "hlp": "help",
        "ppl": "people",
        "fd": "food",
        "med": "medical",
        "nd": "and",
        "ukd": "uttarakhand"
    }

    for k, v in slang_dict.items():
        text = text.replace(k, v)

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

train["clean_text"] = train["tweet_text"].apply(clean_text)
test["clean_text"] = test["tweet_text"].apply(clean_text)

# =========================
# 🔹 Vectorization
# =========================
vectorizer = TfidfVectorizer(
    max_features=8000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train = vectorizer.fit_transform(train["clean_text"])
X_test = vectorizer.transform(test["clean_text"])

y_train = train["class_label"]
y_test = test["class_label"]

# =========================
# 🔹 Model
# =========================
model = LogisticRegression(max_iter=500, class_weight="balanced")
model.fit(X_train, y_train)

# =========================
# 🔹 Evaluate
# =========================
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# =========================
# 🔹 Save
# =========================
joblib.dump(model, "model/model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("✅ Model trained & saved!")