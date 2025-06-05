from openai import OpenAI
import os
from dotenv import load_dotenv
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_domain(text: str) -> str:
    prompt = f"""
You are classifying the domain of this content for scoring purposes.

Here are possible domains:
- self-help
- politics
- tech
- health
- education
- entertainment
- finance
- science
- spirituality
- general

Transcript:
\"\"\"{text}\"\"\"

Respond with only the most relevant domain from the list.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        domain = response.choices[0].message.content.strip().lower()
        return domain
    except Exception as e:
        print("Error inferring domain:", e)
        return "general"
