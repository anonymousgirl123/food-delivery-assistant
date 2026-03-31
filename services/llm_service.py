import re
import openai
import json

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



openai.api_key = "YOUR_API_KEY"

def extract_intent(message: str):
    prompt = f"""
    Extract user intent from the following message.

    Return JSON with:
    - mood (comfort, healthy, treat, craving, neutral)
    - budget (number or null)
    - cuisine (if mentioned)
    - meal_time (breakfast, lunch, dinner, snack or null)

    Message: "{message}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an intent extraction engine."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message["content"]

    try:
        return json.loads(content)
    except:
        return {"mood": "neutral"}
