import re

def detect_mood(message: str):
    message = message.lower()

    if any(word in message for word in ["tired", "sad", "stressed"]):
        return "comfort"

    if any(word in message for word in ["happy", "celebrate"]):
        return "treat"

    if any(word in message for word in ["healthy", "fit", "diet"]):
        return "healthy"

    if any(word in message for word in ["spicy", "craving"]):
        return "craving"

    return "neutral"



def extract_budget(message: str):
    # detect numbers like 200, 300 etc.
    match = re.search(r'(\d+)', message)
    if match:
        return int(match.group(1))
    return None

def extract_intent(message: str):
    intent = {
        "text": message,
        "mood": detect_mood(message),
        "budget": extract_budget(message)
    }

    return intent

