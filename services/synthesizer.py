from config.gemini_client import client
import json


def synthesize(results):
    prompt = f"""
Combine these responses into one coherent answer.

Responses:
{json.dumps(results, indent=2)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text