def extract_intent(message: str):
    message = message.lower()
    intent = {"meal_time": None, "cuisine": None, "budget": None, "taste": None}

    if "breakfast" in message: intent["meal_time"] = "breakfast"
    elif "lunch" in message: intent["meal_time"] = "lunch"
    elif "dinner" in message: intent["meal_time"] = "dinner"

    if "cheap" in message: intent["budget"] = "low"
    if "spicy" in message: intent["taste"] = "spicy"

    return intent
