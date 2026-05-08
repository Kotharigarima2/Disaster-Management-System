import pandas as pd
import json
import pickle

from preprocessing import clean_text

# -------------------------------
# LOAD TEST DATA
# -------------------------------
with open("data/test.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)

df_test = pd.DataFrame(test_data)

# Keep relevant columns
df_test = df_test[['text', 'class_label', 'lang']]

# Keep only English
df_test = df_test[df_test['lang'] == 'en']

# Convert labels to binary
def convert_label(label):
    if label == "not_humanitarian":
        return 0
    return 1

df_test['target'] = df_test['class_label'].apply(convert_label)

df_test = df_test[['text', 'target']]

print("Test dataset:", df_test.shape)

# -------------------------------
# LOAD MODEL
# -------------------------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# -------------------------------
# CLEAN TEXT
# -------------------------------
df_test['cleaned_text'] = df_test['text'].apply(clean_text)

# -------------------------------
# VECTORIZE
# -------------------------------
X_test = vectorizer.transform(df_test['cleaned_text']).toarray()
y_test = df_test['target']

# -------------------------------
# PREDICT
# -------------------------------
y_pred = model.predict(X_test)

# -------------------------------
# EVALUATE
# -------------------------------
from sklearn.metrics import accuracy_score, classification_report

print("Test Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))