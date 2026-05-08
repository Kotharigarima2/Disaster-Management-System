import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from preprocessing import clean_text
from utils import vectorize_data

# load data
df = pd.read_csv("data/final_dataset.csv")

# clean text
df['cleaned_text'] = df['text'].apply(clean_text)

# split
X_train, X_test, y_train, y_test = train_test_split(
    df['cleaned_text'],
    df['target'],
    test_size=0.2,
    random_state=42
)

# vectorize
X_train_vec, X_test_vec, vectorizer = vectorize_data(X_train, X_test)

# train
model = LogisticRegression(max_iter=300)
model.fit(X_train_vec, y_train)

# predict
y_pred = model.predict(X_test_vec)

# evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))

# save
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model saved")

extra_data = pd.DataFrame({
    'text': [
        "forest fire spreading rapidly",
        "volcanic eruption happening",
        "building collapsed due to earthquake",
        "people injured in landslide",
        "massive fire in forest area"
    ],
    'target': [1, 1, 1, 1, 1]
})

df = pd.concat([df, extra_data], ignore_index=True)