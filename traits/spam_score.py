from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_spam_score(text: str) -> dict:
    prompt = f"""
You are analyzing a piece of content for its *Spam Score*.

Text:
\"\"\"{text}\"\"\"

Definition:
Spam Score reflects how repetitive, regurgitated, or low-effort this content is — especially compared to other similar content available online.

Score from -5 to +5:
- -5 = Highly original, strong signal, clearly non-generic
-  0 = Familiar topic, but decently made
- +5 = Generic, formulaic, overused — low-effort content clone

Return a JSON object like:
{{ "spam_score": score (int) }}
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
        print("Error scoring spam score:", e)
        print("GPT output:", content)
        return {"spam_score": None}
