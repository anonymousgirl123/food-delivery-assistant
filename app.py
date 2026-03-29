from fastapi import FastAPI
from models import Request
from services.llm_service import extract_intent
from services.user_service import get_user_profile
from services.context_builder import build_context
from services.recommender import get_food_candidates
from services.response_generator import generate_response

app = FastAPI()


@app.post("/recommend")
def recommend(req: Request):
    # 1. Extract intent from user message
    intent = extract_intent(req.message)

    # 2. Fetch user profile (REAL preferences)
    user = get_user_profile(req.user_id)

    # fallback if user has no preferences
    user_prefs = {
        "favorite_cuisines": user.get("favorite_cuisines", [])
    } if user else {"favorite_cuisines": []}

    # 3. Build dynamic context (weather, time, etc.)
    context = build_context(intent)

    # 4. Get ranked recommendations (already scored inside)
    recommendations = get_food_candidates(
        intent,
        user_prefs=user_prefs,
        context=context
    )

    # 5. Generate response using top results
    reply = generate_response(recommendations[:5])

    return {
        "intent": intent,
        "context": context,
        "recommendations": recommendations[:5],
        "reply": reply
    }
    