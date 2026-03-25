from db.database import SessionLocal
from db.models import FoodItem

def get_food_candidates(intent):
    db = SessionLocal()

    query = db.query(FoodItem)

    if intent.get("meal_time"):
        query = query.filter(FoodItem.type == intent["meal_time"])

    if intent.get("cuisine"):
        query = query.filter(FoodItem.cuisine == intent["cuisine"])

    return [
        {
            "name": f.name,
            "cuisine": f.cuisine,
            "price": f.price,
            "type": f.type
        }
        for f in query.all()
    ]
    