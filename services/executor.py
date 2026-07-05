from config.gemini_client import client


def execute_task(task, model_name):
    prompt = task["description"]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "taskId": task["taskId"],
        "model": model_name,
        "response": response.text
    }