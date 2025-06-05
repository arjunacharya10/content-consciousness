import os
import json
from full_profile import generate_trait_profile

INPUT_FOLDER = "transcripts"

def run_batch_scoring():
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".txt"):
            txt_path = os.path.join(INPUT_FOLDER, file)
            json_path = txt_path.replace(".txt", ".json")

            with open(txt_path, "r") as f:
                text = f.read()

            print(f"Scoring: {file}")
            profile = generate_trait_profile(text, file)
            with open(json_path, "w") as out:
                json.dump(profile, out, indent=2)
            print(f"Saved: {json_path}")

if __name__ == "__main__":
    run_batch_scoring()
