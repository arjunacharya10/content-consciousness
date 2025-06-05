import os
import json
import re
from traits.information_depth import score_information_depth
from traits.attention_quality import score_attention_quality
from traits.value_per_minute import score_value_per_minute
from traits.novelty_index import score_novelty_index
from traits.spam_score import score_spam_score
from traits.perspective_awareness import score_perspective_awareness
from traits.polarity_potential import score_polarity_potential
from utils.domain_classifier import classify_domain
from utils.overall_score import compute_overall_score

def generate_trait_profile(text: str, filename: str) -> dict:
    profile = {}

    # Domain classification
    domain = classify_domain(text)
    profile["domain"] = domain

    # Descriptive metadata
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    profile["description"] = " ".join(sentences[:3]) + ("..." if len(sentences) > 3 else "")
    profile["full_text"] = text
    profile["filename"] = filename

    # Trait scoring
    profile.update(score_information_depth(text))
    profile.update(score_attention_quality(text))
    profile.update(score_value_per_minute(text))
    profile.update(score_novelty_index(text, domain))
    profile.update(score_spam_score(text))
    profile.update(score_perspective_awareness(text))
    profile.update(score_polarity_potential(text))

    # Placeholder for future
    profile["channel_diversity"] = None
    profile["overall_score"] = compute_overall_score(profile)

    return profile
