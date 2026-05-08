import pandas as pd
import os

# Base directory = backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data folder path
data_dir = os.path.join(BASE_DIR, "data")

def get_disaster(event):
    event = event.lower()
    
    if "earthquake" in event:
        return "Earthquake"
    elif "flood" in event:
        return "Flood"
    elif "hurricane" in event or "typhoon" in event:
        return "Cyclone"
    elif "fire" in event:
        return "Fire"
    else:
        return "Other"

def load_data():
    train_df = pd.read_json(os.path.join(data_dir, "train.json"))
    dev_df = pd.read_json(os.path.join(data_dir, "dev.json"))
    test_df = pd.read_json(os.path.join(data_dir, "test.json"))

    train_df = train_df[["text", "event"]]
    dev_df = dev_df[["text", "event"]]
    test_df = test_df[["text", "event"]]

    train_df["label"] = train_df["event"].apply(get_disaster)
    dev_df["label"] = dev_df["event"].apply(get_disaster)
    test_df["label"] = test_df["event"].apply(get_disaster)

    return train_df, dev_df, test_df