from db.database import SessionLocal
from db.models import FoodItem


def calculate_score_and_reason(food, intent, user_prefs, context):
    score = 0
    reasons = []

    # 1. Preference match
    if food.cuisine in user_prefs.get("favorite_cuisines", []):
        score += 40
        reasons.append(f"matches your preference for {food.cuisine} food")

    # 2. Budget match
    if intent.get("budget"):
        if food.price <= intent["budget"]:
            score += 20
            reasons.append("fits your budget")

    # 3. Weather match
    weather = context.get("weather")

    if weather == "rainy" and food.type in ["soup", "hot"]:
        score += 20
        reasons.append("great for rainy weather")

    elif weather == "hot" and food.type in ["cold", "drink"]:
        score += 20
        reasons.append("refreshing for hot weather")

    # 4. Meal time match
    if intent.get("meal_time") == food.type:
        score += 20
        reasons.append(f"perfect for {food.type}")

    return score, reasons


def get_food_candidates(intent, user_prefs={}, context={}):
    db = SessionLocal()
    query = db.query(FoodItem)

    # existing filters
    if intent.get("meal_time"):
        query = query.filter(FoodItem.type == intent["meal_time"])

    if intent.get("cuisine"):
        query = query.filter(FoodItem.cuisine == intent["cuisine"])

    foods = query.all()

    results = []

    for food in foods:
        score, reasons = calculate_score_and_reason(food, intent, user_prefs, context)

        results.append({
            "name": food.name,
            "cuisine": food.cuisine,
            "price": food.price,
            "type": food.type,
            "score": score,
            "reason": ", ".join(reasons) if reasons else "popular choice"
        })

    # sort by score
    ranked = sorted(results, key=lambda x: x["score"], reverse=True)

    return ranked[:5]

#     Expected Response
# [
#   {
#     "name": "Tomato Soup",
#     "score": 80,
#     "reason": "great for rainy weather, fits your budget"
#   },
#   {
#     "name": "Paneer Tikka",
#     "score": 60,
#     "reason": "matches your preference for Indian food"
#   }
# ]
