import json

def build_rich_text(place):
    parts = []

    parts.append(place["name"])


    type_phrases = {
        "eco":        "eco-tourism sustainable travel green destination",
        "wildlife":   "wildlife sanctuary animal spotting nature reserve",
        "cultural":   "cultural heritage local traditions indigenous community",
        "adventure":  "adventure activities outdoor exploration thrill",
        "historical": "historical heritage ancient monuments history archaeology",
        "religious":  "religious pilgrimage sacred site temple monastery",
        "nature":     "nature scenic landscape forest hills valley",
        "leisure":    "leisure relaxation sightseeing tourism",
        "heritage":   "historical heritage ancient monuments",  
    }
    for t in place["types"]:
        parts.append(type_phrases.get(t.lower(), t))

    parts.append("activities include " + ", ".join(place["activities"]))

    parts.append(place["description"])


    avg = (place["budget_min"] + place["budget_max"]) / 2
    if avg < 1000:
        parts.append("budget friendly low cost affordable")
    elif avg > 3500:
        parts.append("premium experience higher budget")

    months = place.get("best_months", [])
    if set(months) & {"Dec", "Jan", "Feb"}:
        parts.append("winter travel cold weather")
    if set(months) & {"Mar", "Apr", "May"}:
        parts.append("spring season pleasant weather")
    if set(months) & {"Jun", "Jul", "Aug"}:
        parts.append("monsoon season lush green")
    if set(months) & {"Sep", "Oct", "Nov"}:
        parts.append("autumn season mild weather")

    return " ".join(parts)


with open("/Users/subhamdas/Desktop/Hackathon/hackdays/pythonServer/ai_services/data/places.json") as f:
    places = json.load(f)

for p in places:
    p["combined_text"] = build_rich_text(p)

with open("/Users/subhamdas/Desktop/Hackathon/hackdays/pythonServer/ai_services/data/places.json", "w") as f:
    json.dump(places, f, indent=2, ensure_ascii=False)

print("Done. Delete place_embeddings.pkl if it exists.")