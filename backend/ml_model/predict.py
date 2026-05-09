import joblib
import re

# =========================
# 🔹 Load Model & Vectorizer
# =========================
import os

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "model", "model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "model", "vectorizer.pkl"))

# =========================
# 🔹 Clean Text
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+|#\w+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# =========================
# 🔹 Keyword Detection
# =========================
def detect_needs(text):
    needs = []

    # Food
    if re.search(r"\b(food|hungry|starving|eat|nothing to eat|no food)\b", text, re.I):
        needs.append("Food 🍞")

    # Water
    if re.search(r"\b(water|thirst|drinking)\b", text, re.I):
        needs.append("Water 💧")

    # Medical
    if re.search(r"\b(medical|doctor|injured|hospital|dead|killed|wounded|aid)\b", text, re.I):
        needs.append("Medical Help 🏥")

    # Shelter
    if re.search(r"\b(shelter|home|homeless|destroyed|collapse)\b", text, re.I):
        needs.append("Shelter 🏠")

    # Search & Rescue
    if re.search(r"\b(missing|found|search and rescue|rescue operations)\b", text, re.I):
        needs.append("Search & Rescue 🔍")

    # Emotional Support
    if re.search(r"\b(emotional support|counseling|mental help|trauma)\b", text, re.I):
        needs.append("Emotional Support ❤️")

    # General Help ONLY if no negation like "no need", "safe", "fine"
    if re.search(r"\b(help|urgent|relief|donate)\b", text, re.I):
        if not re.search(r"\b(no need|safe|fine|okay|nothing required)\b", text, re.I):
            needs.append("General Help 🤝")

    return list(set(needs))
# =========================
# 🔹 Model Mapping
# =========================
def map_label_to_needs(label):
    mapping = {
        "injured_or_dead_people": ["Medical Help 🏥"],
        "rescue_volunteering_or_donation_effort": ["Food 🍞", "Water 💧", "General Help 🤝"],
        "infrastructure_and_utility_damage": ["Shelter 🏠"],
        "sympathy_and_support": ["Emotional Support ❤️"],
        "affected_people": ["General Help 🤝"],
        "missing_or_found_people": ["Search & Rescue 🔍"],
        "other_relevant_information": []
    }
    return mapping.get(label, [])

# =========================
# 🔹 No Need Logic
# =========================
# =========================
# 🔹 No Need Logic (Improved)
# =========================
def is_no_need(text):
    return bool(re.search(
        r"\b(no need( anything| now| at all)?|nothing needed|no help required|safe|fine|okay|all good)\b",
        text
    ))

def is_general_help(text):
    return bool(re.search(
        r"\b(need help|help needed|urgent help|require help)\b",
        text
    ))
# =========================
# 🔹 Predict Function (used by Flask)
# =========================
def predict(text):
    cleaned = clean_text(text)

    # 1️⃣ No Need
    if is_no_need(cleaned):
        return ["No Need ❌"]

    # 2️⃣ Keyword detection
    keyword_needs = detect_needs(cleaned)
    if keyword_needs:
        return keyword_needs

    # 3️⃣ Model prediction
    vec = vectorizer.transform([cleaned])
    label = model.predict(vec)[0]
    model_needs = map_label_to_needs(label)

    if model_needs:
        return model_needs

    # 4️⃣ STRICT General Help (ONLY if clearly written)
    if is_general_help(cleaned):
        return ["General Help 🤝"]

    # 5️⃣ FINAL fallback
    return ["Required Info ⚠️"]

# =========================
# 🔹 Command-line Test
# =========================
if __name__ == "__main__":
    tweet = input("Enter tweet: ")
    print("Detected Needs:", ", ".join(predict(tweet)))