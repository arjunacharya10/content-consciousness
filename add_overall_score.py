import os
import json
from utils.overall_score import compute_overall_score

INPUT_FOLDER = "transcripts"

def update_scores():
    updated = 0
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".json"):
            path = os.path.join(INPUT_FOLDER, file)
            with open(path) as f:
                profile = json.load(f)

            if "overall_score" in profile:
                continue

            profile["overall_score"] = compute_overall_score(profile)

            with open(path, "w") as f:
                json.dump(profile, f, indent=2)

            updated += 1

    print(f"✅ Updated {updated} files with overall_score")

if __name__ == "__main__":
    update_scores()
