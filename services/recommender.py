from db.database import SessionLocal
from db.models import FoodItem

def calculate_score(food, intent, user_prefs, context):
    score = 0

    # 1. Preference match (highest weight)
    if food.cuisine in user_prefs.get("favorite_cuisines", []):
        score += 40

    # 2. Budget match
    if intent.get("budget"):
        if food.price <= intent["budget"]:
            score += 20

    # 3. Weather match (simple logic)
    weather = context.get("weather")

    if weather == "rainy" and food.type in ["soup", "hot"]:
        score += 20
    elif weather == "hot" and food.type in ["cold", "drink"]:
        score += 20

    # 4. Meal time match
    if intent.get("meal_time") == food.type:
        score += 20

    return score


def get_food_candidates(intent, user_prefs={}, context={}):
    db = SessionLocal()
    query = db.query(FoodItem)

    # basic filtering (keep your logic)
    if intent.get("meal_time"):
        query = query.filter(FoodItem.type == intent["meal_time"])

    if intent.get("cuisine"):
        query = query.filter(FoodItem.cuisine == intent["cuisine"])

    foods = query.all()

    # 🔥 NEW: scoring + ranking
    scored_results = []
    for food in foods:
        score = calculate_score(food, intent, user_prefs, context)

        scored_results.append({
            "name": food.name,
            "cuisine": food.cuisine,
            "price": food.price,
            "type": food.type,
            "score": score
        })

    # sort by score (descending)
    ranked_results = sorted(scored_results, key=lambda x: x["score"], reverse=True)

    return ranked_results[:5]  # top 5
    