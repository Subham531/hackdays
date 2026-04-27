from fastapi import APIRouter, HTTPException
from recommender.api.ingestion import normalise
import json, os

router = APIRouter()
DATA_PATH = "data/places.json"

def load_places():
    with open(DATA_PATH) as f:
        return json.load(f)

def save_places(places):
    with open(DATA_PATH, "w") as f:
        json.dump(places, f, indent=2, ensure_ascii=False)

def bust_cache():
    cache = "data/place_embeddings.pkl"
    if os.path.exists(cache):
        os.remove(cache)

@router.post("/ingest", status_code=201)
def ingest(payload: dict):
    try:
        normalised = normalise(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Missing field: {e}")

    places = load_places()

    # deduplicate by their post ID
    if any(p["place_id"] == normalised["place_id"] for p in places):
        raise HTTPException(status_code=409, detail=f"Post ID {normalised['place_id']} already exists")

    places.append(normalised)
    save_places(places)
    bust_cache()

    return {
        "status": "ok",
        "place_id": normalised["place_id"],
        "name": normalised["name"],
        "post_type": normalised["post_type"]
    }