from datetime import datetime

CURRENT_MONTH = datetime.now().strftime("%b")

def filter_candidates(places, budget=None, month=None, types=None, state=None):
    results = []
    for p in places:
        best_months = p.get("best_months") or []

        if budget is not None:
            if not (p.get("budget_min", 0) <= budget <= p.get("budget_max", 9999)):
                continue

        if month is not None:
            if best_months and month not in best_months:
                continue

        if types is not None:
            place_types = p.get("types") or []
            if not any(t in place_types for t in types):
                continue

        if state is not None:
            place_state = (p.get("state") or "").lower().strip()
            if place_state and place_state != state.lower().strip():
                continue

        results.append(p)

    return results if results else places  