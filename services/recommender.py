FOODS = [
    {"name": "Biryani", "cuisine": "indian", "price": 200, "type": "lunch"},
    {"name": "Dosa", "cuisine": "indian", "price": 100, "type": "breakfast"},
]

def get_food_candidates(intent):
    return FOODS

def rank_foods(candidates, context, user):
    return candidates
