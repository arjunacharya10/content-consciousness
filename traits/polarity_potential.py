from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_polarity_potential(text: str) -> dict:
    prompt = f"""
You're an expert content analyst scoring the *Polarity Potential* of a text.

Text:
\"\"\"{text}\"\"\"

Polarity Potential reflects the likelihood that the content will provoke strong tribal or ideological division, outrage, or identity-based reactions.

Score from -5 to +5:
- -5: Encourages civil disagreement; invites thoughtful discourse
-  0: Neutral, unlikely to provoke polarization
- +5: Highly polarizing; uses outrage-bait, strawman attacks, or divisive framing

Return a JSON object like:
{{ "polarity_potential": score (int) }}
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
        print("Error scoring polarity potential:", e)
        print("GPT output:", content)
        return {"polarity_potential": None}
