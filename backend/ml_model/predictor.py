import joblib
import re
import os

BASE = os.path.dirname(__file__)

# =========================
# 🔹 LOAD MODELS
# =========================
need_model = joblib.load(os.path.join(BASE, "model", "need_model.pkl"))
type_model = joblib.load(os.path.join(BASE, "model", "type_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE, "model", "vectorizer.pkl"))

# =========================
# 🔹 CLEAN TEXT
# =========================
def clean(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# =========================
# 🔥 DISASTER EXTRACTION
# =========================
def extract_disaster_name(text):

    text = str(text).lower()

    mapping = {
        "earthquake": "Earthquake 🌍",
        "flood": "Flood 🌊",
        "floods": "Flood 🌊",
        "hurricane": "Hurricane 🌪️",
        "cyclone": "Cyclone 🌀",
        "typhoon": "Typhoon 🌀",
        "tornado": "Tornado 🌪️",
        "explosion": "Explosion 💥",
        "blast": "Explosion 💥",
        "fire": "Fire 🔥",
        "wildfire": "Wildfire 🔥",
        "volcano": "Volcanic Eruption 🌋",
        "landslide": "Landslide ⛰️",
        "shooting": "Mass Shooting 🔫"
    }

    for key, value in mapping.items():
        if key in text:
            return value

    # 🔥 FIX 1: NOT MENTIONED CASE
    return "Not Mentioned ⚠️"

# =========================
# 🔹 NEED MAPPING
# =========================
def map_needs(label):
    mapping = {
        "injured_or_dead_people": ["Medical Help 🏥"],
        "requests_or_needs": ["Food 🍞", "Water 💧", "General Help 🤝"],
        "infrastructure_and_utility_damage": ["Shelter 🏠"],
        "sympathy_and_support": ["Emotional Support ❤️"],
        "displaced_and_evacuations": ["Shelter 🏠"],
        "affected_individual": ["Search & Rescue 🔍"],
        "donation_and_volunteering": ["Food 🍞", "Water 💧", "General Help 🤝"],
        "response_efforts": ["General Help 🤝"]
    }
    return mapping.get(label, [])

# =========================
# 🔹 PRIORITY
# =========================
def priority(needs):

    if "Medical Help 🏥" in needs or "Search & Rescue 🔍" in needs:
        return "HIGH 🚨"

    if "Food 🍞" in needs or "Water 💧" in needs:
        return "MEDIUM ⚠️"

    if not needs or needs == ["No Need ❌"]:
        return "LOW ℹ️"

    return "LOW ℹ️"

# =========================
# 🔥 MAIN FUNCTION
# =========================
def predict_all(text):

    cleaned = clean(text)
    vec = vectorizer.transform([cleaned])

    # =========================
    # 1️⃣ DISASTER TYPE
    # =========================
    ml_type = type_model.predict(vec)[0]
    event_type = extract_disaster_name(text)

    dtype = event_type if event_type != "Not Mentioned ⚠️" else ml_type

    # =========================
    # 2️⃣ NEEDS
    # =========================
    label = need_model.predict(vec)[0]
    needs = map_needs(label)

    # 🔥 FIX 2: NO NEED CASE
    if not needs:
        needs = ["No Need ❌"]

    # =========================
    # 3️⃣ OUTPUT
    # =========================
    return {
        "disaster": "YES ⚠️" if event_type != "Not Mentioned ⚠️" else "NO ❌",
        "type": dtype,
        "needs": needs,
        "priority": priority(needs)
    }

# =========================
# 🔹 TEST
# =========================
if __name__ == "__main__":
    text = input("Enter text: ")
    result = predict_all(text)

    print("\n🔍 RESULT")
    print("Disaster:", result["disaster"])
    print("Type:", result["type"])
    print("Needs:", ", ".join(result["needs"]))
    print("Priority:", result["priority"])