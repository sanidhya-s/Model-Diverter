from google.genai import types
from config.gemini_client import client
import json


def decompose_prompt(user_prompt, taxonomy):
    prompt = f"""
Break the prompt into independent tasks.

Taxonomy:
{json.dumps(taxonomy, indent=2)}

Prompt:
{user_prompt}

Return ONLY JSON:

{{
  "tasks": [
    {{
      "taskId": 1,
      "description": "",
      "categoryId": "",
      "subCategory": "",
      "dependsOn": []
    }}
  ]
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