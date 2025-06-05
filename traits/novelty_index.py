from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_novelty_index(text: str, domain: str = "general") -> dict:
    prompt = f"""
You are evaluating a transcript for its *Novelty Index*.

Transcript:
\"\"\"{text}\"\"\"

Domain: {domain}

Definition:
Novelty Index measures how original or uncommon this content is compared to other content in the same domain. It rewards fresh phrasing, unique angles, or rare combinations of ideas. It penalizes cliché phrasing, formulaic tips, or "seen a hundred times" formats.

Score from -5 to +5:
- +5 = Extremely novel, very rare ideas or style
-  0 = Common but not repetitive
- -5 = Highly repetitive, low originality, saturated format

Return a JSON object like:
{{ "novelty_index": score (int) }}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.choices[0].message.content
        json_string = re.search(r'\{.*\}', content, re.DOTALL).group(0)
        score = json.loads(json_string)
        return score
    except Exception as e:
        print("Error scoring novelty index:", e)
        print("GPT output:", content)
        return {"novelty_index": None}
