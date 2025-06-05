from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_attention_quality(text: str) -> dict:
    prompt = f"""
You are evaluating a piece of content for its *Attention Quality*.

Text:
\"\"\"{text}\"\"\"

Definition:
Attention Quality reflects how well the content supports focused, sustained, and mentally coherent attention. It rewards immersive and structured content and penalizes scattered, overstimulating, or chaotic delivery.

Score from -5 to +5:
- +5 = Calming, immersive, easy to focus on
-  0 = Neutral structure and pacing
- -5 = Mentally chaotic, overstimulating, likely to fragment attention

Return a JSON object like:
{{ "attention_quality": score (int) }}
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
        print("Error scoring attention quality:", e)
        print("GPT output:", content)
        return {"attention_quality": None}
