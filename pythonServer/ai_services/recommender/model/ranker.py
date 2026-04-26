from recommender.model.scoring import compute_eco_score, compute_popularity
from recommender.model.similarity import build_place_corpus, compute_similarity

def enrich_places(places):
    for place in places:
        if "best_months" not in place:
            place["best_months"] = []          # guard against kisama_22
        place["eco_score"] = compute_eco_score(place)
        place["popularity"] = compute_popularity(place)
    return places
    
def compute_final_score(place, similarity):
    return (
        similarity * 0.5 +
        (place["eco_score"] / 100) * 0.3 +
        (place["popularity"] / 100) * 0.2
    )

def rank_places(user_query, places):
    places = enrich_places(places)
    place_embeddings = build_place_corpus(places)  # encode all 100 places once
    similarities = compute_similarity(user_query, place_embeddings)

    for i, place in enumerate(places):
        place["similarity"] = similarities[i]
        place["final_score"] = compute_final_score(place, similarities[i])

    return sorted(places, key=lambda x: x["final_score"], reverse=True)