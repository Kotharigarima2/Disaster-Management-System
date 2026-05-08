import pandas as pd
import json

# -------------------------------
# 1. LOAD CRISIS DATA (train.json)
# -------------------------------
with open("data/train.json", "r", encoding="utf-8") as f:
    crisis_data = json.load(f)

df_crisis = pd.DataFrame(crisis_data)

print("Original Crisis Data:", df_crisis.shape)

# -------------------------------
# 2. KEEP IMPORTANT COLUMNS
# -------------------------------
df_crisis = df_crisis[['text', 'class_label', 'lang']]

# -------------------------------
# 3. FILTER ONLY ENGLISH
# -------------------------------
df_crisis = df_crisis[df_crisis['lang'] == 'en']

# -------------------------------
# 4. CONVERT LABELS TO BINARY
# -------------------------------
def convert_label(label):
    if label == "not_humanitarian":
        return 0
    return 1

df_crisis['target'] = df_crisis['class_label'].apply(convert_label)

df_crisis = df_crisis[['text', 'target']]

print("Cleaned Crisis Data:", df_crisis.shape)

# -------------------------------
# 5. LOAD KAGGLE DATA (tweets.csv)
# -------------------------------
df_kaggle = pd.read_csv("data/tweets.csv")

df_kaggle = df_kaggle[['text', 'target']]

print("Kaggle Data:", df_kaggle.shape)

# -------------------------------
# 6. COMBINE BOTH
# -------------------------------
df = pd.concat([df_kaggle, df_crisis], ignore_index=True)

# -------------------------------
# 7. BASIC CLEANING
# -------------------------------
df = df.dropna(subset=['text'])
df['text'] = df['text'].astype(str)

# remove very small text
df = df[df['text'].str.len() > 15]

# remove duplicates
df = df.drop_duplicates(subset='text')

# shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print("Final Dataset:", df.shape)

# -------------------------------
# 8. SAVE FINAL DATA
# -------------------------------
df.to_csv("data/final_dataset.csv", index=False)

print("✅ final_dataset.csv created")
