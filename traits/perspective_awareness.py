from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_perspective_awareness(text: str) -> dict:
    prompt = f"""
You are analyzing a piece of content for *Perspective Awareness*.

Text:
\"\"\"{text}\"\"\"

Definition:
Perspective Awareness reflects how fairly the content acknowledges and engages with opposing or alternate views.

Score from -5 to +5:
- +5 = Engages with multiple perspectives respectfully
-  0 = Presents only one side without aggression
- -5 = Misrepresents, mocks, or attacks opposing views

Return a JSON object like:
{{ "perspective_awareness": score (int) }}
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
        print("Error scoring perspective awareness:", e)
        print("GPT output:", content)
        return {"perspective_awareness": None}
