from db.database import SessionLocal
from db.models import User

def get_user_profile(user_id: str):
    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {
            "preferred_cuisines": ["indian"],
            "veg": True,
            "past_orders": []
        }

    return {
        "preferred_cuisines": [user.preferred_cuisine],
        "veg": user.veg,
        "past_orders": []
    }
    