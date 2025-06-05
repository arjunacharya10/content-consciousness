import os
import json
import argparse
from full_profile import generate_trait_profile

INPUT_FOLDER = "transcripts"

def run_batch_scoring(skip_existing: bool):
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".txt"):
            txt_path = os.path.join(INPUT_FOLDER, file)
            json_path = txt_path.replace(".txt", ".json")

            if skip_existing and os.path.exists(json_path):
                print(f"Skipping (already scored): {file}")
                continue

            with open(txt_path, "r") as f:
                text = f.read()

            print(f"Scoring: {file}")
            profile = generate_trait_profile(text, file)
            with open(json_path, "w") as out:
                json.dump(profile, out, indent=2)
            print(f"Saved: {json_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run trait scoring for all transcripts.")
    parser.add_argument(
        "--force", action="store_true",
        help="Reprocess all files even if output JSON already exists"
    )
    args = parser.parse_args()

    run_batch_scoring(skip_existing=not args.force)
