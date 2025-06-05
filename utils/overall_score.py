# utils/overall_score.py

def compute_overall_score(profile: dict) -> float:
    weights = {
        "information_depth": 0.25,
        "attention_quality": 0.25,
        "value_per_minute": 0.2,
        "novelty_index": 0.15,
        "perspective_awareness": 0.15,
        "spam_score": -0.3
    }

    overall = 0
    for trait, weight in weights.items():
        score = profile.get(trait, 0) or 0
        overall += weight * score

    return round(overall, 2)
