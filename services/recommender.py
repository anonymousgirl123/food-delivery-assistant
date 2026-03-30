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
    # Budget scoring
    # "Suggest something spicy under 150"
    # [
    #     {
    #         "name": "Paneer Roll",
    #         "price": 120,
    #         "score": 85,
    #         "reason": "fits your budget, matches your preference for Indian food"
    #     }
    # ]
    if intent.get("budget"):
        if food.price <= intent["budget"]:
            score += 20
            reasons.append("fits your budget")
        else:
            score -= 10
            reasons.append("slightly above your budget")

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

    # Mood-based scoring
    mood = intent.get("mood")

    if mood == "comfort" and food.type in ["hot", "soup"]:
        score += 20
        reasons.append("good for a comforting mood")

    elif mood == "healthy" and food.type in ["salad", "light"]:
        score += 20
        reasons.append("fits your healthy mood")

    elif mood == "treat" and food.type in ["dessert"]:
        score += 20
        reasons.append("perfect for a treat")

    elif mood == "craving":
        score += 10
        reasons.append("satisfies your craving")

    return score, reasons


def get_food_candidates(intent, user_prefs={}, context={}):
    db = SessionLocal()
    query = db.query(FoodItem)

    # existing filters
    if intent.get("meal_time"):
        query = query.filter(FoodItem.type == intent["meal_time"])

    if intent.get("cuisine"):
        query = query.filter(FoodItem.cuisine == intent["cuisine"])

    if intent.get("budget"):
        query = query.filter(FoodItem.price <= intent["budget"])

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

    top_items = ranked[:10]

    combo = generate_combo_meal(top_items)

    return {
        "items": ranked[:5],
        "combo": combo
    }

    # return ranked[:5]

def generate_combo_meal(foods):
    main = None
    drink = None
    side = None

    # pick best items by category
    for food in foods:
        if food.get("category") == "main" and not main:
            main = food
        elif food.get("category") == "drink" and not drink:
            drink = food
        elif food.get("category") == "side" and not side:
            side = food

    combo = {
        "main": main,
        "drink": drink,
        "side": side
    }

    return combo


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
# mood based
# {
#   "name": "Hot Soup",
#   "score": 85,
#   "reason": "good for a comforting mood, great for rainy weather"
# }
