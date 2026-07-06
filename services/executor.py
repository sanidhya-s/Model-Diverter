from pathlib import Path

from config.gemini_client import client
from utils.file_generators import FILE_GENERATORS, detect_requested_file_type
from utils.response_files import save_response_files


def execute_task(task, model_name, docs_dir: Path | None = None, file_prefix: str = ""):
    prompt = task["description"]
    requested_file = detect_requested_file_type(prompt)

    if requested_file in FILE_GENERATORS and docs_dir and file_prefix:
        summary, file_path = FILE_GENERATORS[requested_file](prompt, docs_dir, file_prefix)
        return {
            "taskId": task["taskId"],
            "model": model_name,
            "response": summary,
            "saved_files": [file_path],
        }

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    result = {
        "taskId": task["taskId"],
        "model": model_name,
        "response": response.text or "",
    }

    if docs_dir and file_prefix:
        saved_files = save_response_files(response, docs_dir, file_prefix)
        if saved_files:
            result["saved_files"] = saved_files

    return result
