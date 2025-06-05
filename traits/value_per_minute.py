from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_value_per_minute(text: str, duration_min: float = 5.0) -> dict:
    prompt = f"""
You're evaluating a video transcript for its *Value Per Minute*.

Transcript:
\"\"\"{text}\"\"\"

Definition:
Value Per Minute (VPM) is the amount of meaningful, unique, or actionable content delivered per minute. It rewards density and penalizes content that could be much shorter without losing impact.

The video is {duration_min} minutes long.

Score from -5 to +5:
- +5 = Extremely dense, every minute is useful or insightful
-  0 = Average pacing, some fluff
- -5 = Low signal, wastes viewer's time

Return a JSON object like:
{{ "value_per_minute": score (int) }}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        json_string = re.search(r'\{.*\}', content, re.DOTALL).group(0)
        score = json.loads(json_string)
        return score
    except Exception as e:
        print("Error scoring value_per_minute:", e)
        print("GPT output:", content)
        return {"value_per_minute": None}
