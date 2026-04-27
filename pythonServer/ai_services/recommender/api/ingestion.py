# api/ingestion.py
import uuid
from datetime import datetime

MONTH_ALIASES = {
    "jan": "Jan", "feb": "Feb", "mar": "Mar", "apr": "Apr",
    "may": "May", "jun": "Jun", "jul": "Jul", "aug": "Aug",
    "sep": "Sep", "oct": "Oct", "nov": "Nov", "dec": "Dec"
}

def normalise_months(months: list[str]) -> list[str]:
    return [MONTH_ALIASES.get(m.lower(), m) for m in (months or [])]

def build_combined_text(title, types, activities, description, state):
    type_phrases = {
        "eco":        "eco-tourism sustainable travel green destination",
        "wildlife":   "wildlife sanctuary animal spotting nature reserve",
        "cultural":   "cultural heritage local traditions indigenous community",
        "adventure":  "adventure activities outdoor exploration",
        "historical": "historical heritage ancient monuments",
        "religious":  "religious pilgrimage sacred site temple monastery",
        "nature":     "nature scenic landscape forest hills valley",
        "leisure":    "leisure relaxation sightseeing tourism",
        "heritage":   "historical heritage ancient monuments",
    }
    parts = [title, state or ""]
    for t in (types or []):
        parts.append(type_phrases.get(t.lower(), t))
    if activities:
        parts.append("activities include " + ", ".join(activities))
    parts.append(description or "")
    return " ".join(filter(None, parts))

def normalise(payload: dict) -> dict:
    """
    Accepts the full payload from the team.
    Uses 'post' as the source of truth, 'data' for location.
    """
    post = payload.get("post", {})
    data = payload.get("data", {})          # location lives here

    if not post:
        raise ValueError("Payload missing 'post' object")

    meta     = post.get("metadata", {})
    types    = meta.get("types", [])
    activities = meta.get("activities", [])
    months   = normalise_months(meta.get("months", []))
    state    = post.get("state", "")
    title    = post.get("title", "")
    description = post.get("description", "")
    post_type = post.get("postType", "PLACE").upper()

    # budget comes from post.metadata (camelCase from team)
    budget_min = meta.get("budgetMin", 0)
    budget_max = meta.get("budgetMax", 9999)

    # location only in data, not post
    location = data.get("location", {})

    # images from data
    images = data.get("images", [])

    return {
        "place_id":     post.get("id", str(uuid.uuid4())),   # use their UUID
        "user_id":      post.get("userId", ""),
        "name":         title,
        "state":        state,
        "types":        types,
        "activities":   activities,
        "description":  description,
        "budget_min":   budget_min,
        "budget_max":   budget_max,
        "best_months":  months,
        "location":     location,
        "images":       images,
        "post_type":    post_type,
        "combined_text": build_combined_text(title, types, activities, description, state),
        "created_at":   post.get("createdAt", datetime.utcnow().isoformat()),
    }