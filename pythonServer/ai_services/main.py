import json
from recommender.model.ranker import rank_places
from recommender.model.filters import filter_candidates
from recommender.utils.preprocessing import build_rich_text
def load_places():
    with open("data/places.json") as f:
        places = json.load(f)
    for place in places:
        place["combined_text"] = build_rich_text(place)  
    return places

def recommend(query,state=None, budget=None, month=None, types=None):
    places = load_places()
    candidates = filter_candidates(places, state=state,budget=budget, month=month, types=types)
    ranked = rank_places(query, candidates)
    return ranked[:5]

results = recommend("river rafting",state='Assam')

for r in results:
    print(r["name"], r["state"],r["final_score"])