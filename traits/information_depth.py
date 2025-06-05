from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_information_depth(text: str) -> dict:
    prompt = f"""
You are analyzing the *information depth* of a text article.

Text:
\"\"\"{text}\"\"\"

Rate its **Information Depth** from -5 to +5:
- +5 = Insightful, multi-layered, expert-level explanation
-  0 = Average, surface-level, lacks nuance
- -5 = Misleading, vague, factually weak

Return a JSON object like:
{{ "information_depth": score (int) }}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        try:
            json_string = re.search(r'\{.*\}', content, re.DOTALL).group(0)
            score = json.loads(json_string)
        except Exception as parse_error:
            print("Failed to parse model output:", content)
            raise parse_error
        return score
    except Exception as e:
        print(f"Error scoring depth: {e}")
        return {"information_depth": None}
