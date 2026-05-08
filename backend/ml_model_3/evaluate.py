import pickle
import os
from load_data import load_data
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(BASE_DIR, "models")

model = pickle.load(open(os.path.join(model_dir, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(model_dir, "vectorizer.pkl"), "rb"))

train_df, dev_df, test_df = load_data()

X_test = test_df["text"]
y_test = test_df["label"]

X_test_vec = vectorizer.transform(X_test)
y_pred = model.predict(X_test_vec)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))