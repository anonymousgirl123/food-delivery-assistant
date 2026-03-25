from fastapi import FastAPI
from models import Request
from services.llm_service import extract_intent
from services.user_service import get_user_profile
from services.context_builder import build_context
from services.recommender import get_food_candidates, rank_foods
from services.response_generator import generate_response

app = FastAPI()

@app.post("/recommend")
def recommend(req: Request):
    intent = extract_intent(req.message)
    user = get_user_profile(req.user_id)
    context = build_context(intent)
    candidates = get_food_candidates(intent)
    ranked = rank_foods(candidates, context, user)
    reply = generate_response(ranked)

    return {"intent": intent, "recommendations": ranked[:5], "reply": reply}
