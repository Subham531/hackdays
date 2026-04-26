from datetime import datetime

CURRENT_MONTH = datetime.now().strftime("%b")

def filter_candidates(places, budget=None, month=None, types=None):
    results = []
    for p in places:
        if budget and not (p["budget_min"] <= budget <= p["budget_max"]):
            continue
        if month and month not in p["best_months"]:
            continue
        if types and not any(t in p["types"] for t in types):
            continue
        results.append(p)
    return results if results else places  # fallback: return all if filters too strict