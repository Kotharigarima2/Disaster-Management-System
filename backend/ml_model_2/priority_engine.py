def calculate_priority(tweet_count, disaster_ratio, weather_severity, tweets):

    # 🔥 HARD RULE 1: Extreme case
    if disaster_ratio >= 0.8 and tweet_count >= 2:
        return 5   # HIGH

    # 🔥 HARD RULE 2: Balanced disaster presence
    if disaster_ratio >= 0.5 and tweet_count >= 2:
        return 3   # MEDIUM

    score = 0

    # tweet count
    if tweet_count >= 10:
        score += 2
    elif tweet_count >= 5:
        score += 1

    # ratio
    if disaster_ratio >= 0.6:
        score += 2
    elif disaster_ratio >= 0.3:
        score += 1

    # weather
    score += weather_severity

    # severity keywords
    severe_count = detect_severe_tweets(tweets)
    if severe_count >= 1:
        score += 2

    return score

def detect_accident_severity(tweets):

    for t in tweets:
        t = t.lower()

        if "accident" in t:
            # 🔥 major accident
            if any(word in t for word in ["dead", "death", "killed", "injured"]):
                return "HIGH"
            else:
                return "LOW"

    return None


def get_priority_level(score):
    if score >= 5:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    else:
        return "LOW"
    
def detect_severe_tweets(tweets):
    severe_keywords = [
        "explosion", "blast", "dead", "killed",
        "collapsed", "collapse", "trapped",
        "emergency", "urgent", "rescue",
        "injured", "critical"
    ]

    count = 0

    for t in tweets:
        t = t.lower()
        if any(word in t for word in severe_keywords):
            count += 1

    return count
