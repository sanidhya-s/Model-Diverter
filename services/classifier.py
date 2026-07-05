from google.genai import types
from config.gemini_client import client
import json


def classify_prompt(user_prompt, taxonomy):
    prompt = f"""
Classify the user prompt.

Taxonomy:
{json.dumps(taxonomy, indent=2)}

Prompt:
{user_prompt}

Return ONLY JSON:

{{
  "categoryId": "",
  "subCategory": "",
  "confidence": 0.0
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)