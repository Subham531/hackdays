from fastapi import APIRouter, HTTPException
from recommender.api.schemas import RecommendRequest, RecommendResponse, PlaceResult
from recommender.model.ranker import rank_places
from recommender.model.filters import filter_candidates
import json, os



router = APIRouter()

def load_places():
    path = os.path.join(os.path.dirname(__file__), "/Users/subhamdas/Desktop/Hackathon/hackdays/pythonServer/ai_services/data/places.json")
    with open(path) as f:
        return json.load(f)


@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    try:
        places = load_places()
        candidates = filter_candidates(
            places,
            state= req.state,
            budget=req.budget,
            month=req.month,
            types=req.types
        )
        ranked = rank_places(req.query, candidates)
        top = ranked[:req.top_k]

        return RecommendResponse(
            query=req.query,
            intent=ranked[0].get("_intent") if ranked else None,
            results=[PlaceResult(**p) for p in top]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))