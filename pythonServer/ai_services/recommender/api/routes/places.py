# api/routes/places.py
from fastapi import APIRouter, HTTPException
import json, os

router = APIRouter()
DATA_PATH = "data/places.json"

def load_places():
    with open(DATA_PATH) as f:
        return json.load(f)

@router.get("/places")
def get_all_places():
    places = load_places()
    return {"total": len(places), "places": places}

@router.get("/places/{place_id}")
def get_place(place_id: str):
    places = load_places()
    match = next((p for p in places if p["place_id"] == place_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Place '{place_id}' not found")
    return match

@router.delete("/places/{place_id}")
def delete_place(place_id: str):
    places = load_places()
    filtered = [p for p in places if p["place_id"] != place_id]
    if len(filtered) == len(places):
        raise HTTPException(status_code=404, detail=f"Place '{place_id}' not found")
    with open(DATA_PATH, "w") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)
    # bust cache
    cache = "data/place_embeddings.pkl"
    if os.path.exists(cache):
        os.remove(cache)
    return {"status": "deleted", "place_id": place_id}