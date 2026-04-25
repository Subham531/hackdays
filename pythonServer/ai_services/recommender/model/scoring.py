def compute_eco_score(place):
    eco_type_weight = {
        "eco": 1.0, "nature": 0.8, "wildlife": 0.75,
        "adventure": 0.5, "cultural": 0.4,
        "historical": 0.3, "religious": 0.3, "leisure": 0.35
    }

    eco_activity_weight = {
        "bird watching": 1.0, "nature walk": 1.0,
        "trekking": 0.85, "cycling": 0.9,
        "camping": 0.75, "boating": 0.6,
        "safari": 0.5, "photography": 0.4
    }

    eco_keywords = {
        "eco": 1.0, "forest": 0.9, "rainforest": 1.0,
        "wildlife": 0.85, "biodiversity": 1.0,
        "conservation": 1.0, "river": 0.7,
        "lake": 0.7, "mountain": 0.7, "village": 0.6
    }

    type_scores = [
        eco_type_weight.get(t.lower(), 0.3)
        for t in place["types"]
    ]
    type_score = sum(type_scores) / len(type_scores)

    activity_scores = [
        eco_activity_weight.get(a.lower(), 0.3)
        for a in place["activities"]
    ]
    activity_score = sum(activity_scores) / len(activity_scores)

    text = place["combined_text"].lower()
    keyword_hits = [
        weight for word, weight in eco_keywords.items()
        if word in text
    ]

    keyword_score = (
        sum(keyword_hits) / len(keyword_hits)
        if keyword_hits else 0.3
    )

    eco_score = (
        0.4 * type_score +
        0.3 * activity_score +
        0.3 * keyword_score
    )

    return round(eco_score * 100, 2)


def compute_popularity(place):
    base_popularity = {
    "Kaziranga National Park": 95,
    "Tawang": 90,
    "Cherrapunji (Sohra)": 92,
    "Dawki": 88,
    "Gangtok": 93,
    "Majuli": 85
    }


    base = base_popularity.get(place["name"], 60)


    remote_keywords = ["remote", "offbeat", "high-altitude", "hidden"]
    text = place["combined_text"].lower()

    if any(k in text for k in remote_keywords):
        accessibility = 0.4
    elif "city" in text or "capital" in text:
        accessibility = 1.0
    else:
        accessibility = 0.7


    avg_budget = (place["budget_min"] + place["budget_max"]) / 2
    budget_score = 1 - (avg_budget / 5000)

    popularity = (
        0.6 * base +
        0.2 * (accessibility * 100) +
        0.2 * (budget_score * 100)
    )

    return round(popularity, 2)
