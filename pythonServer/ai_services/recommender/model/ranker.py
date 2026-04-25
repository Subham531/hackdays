from scoring import compute_eco_score, compute_popularity

def enrich_places(places):
    for place in places:
        place["eco_score"] = compute_eco_score(place)
        place["popularity"] = compute_popularity(place)
    return places
