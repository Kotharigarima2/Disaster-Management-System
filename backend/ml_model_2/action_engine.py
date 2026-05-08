def get_action(priority_level):
    
    if priority_level == "HIGH":
        return [
            "🚨 Send emergency alerts",
            "🚑 Deploy rescue teams",
            "🏠 Start evacuation",
            "🚧 Block unsafe areas"
        ]
    
    elif priority_level == "MEDIUM":
        return [
            "⚠️ Issue warning",
            "👀 Monitor situation",
            "🚒 Keep response team ready"
        ]
    
    else:
        return [
            "✅ Situation normal",
            "📊 Continue monitoring"
        ]