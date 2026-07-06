from pathlib import Path

from config.gemini_client import client
import json

from utils.file_generators import FILE_GENERATORS, detect_requested_file_type
from utils.response_files import save_response_files

FILE_LABELS = {
    "pptx": "PowerPoint",
    "docx": "Word document",
}


def _has_file_with_extension(results: list[dict], extension: str) -> bool:
    extension = extension.lower()
    for result in results:
        for saved_file in result.get("saved_files", []):
            if saved_file.lower().endswith(extension):
                return True
    return False


def synthesize(
    results,
    docs_dir: Path | None = None,
    file_prefix: str = "",
    user_prompt: str = "",
):
    prompt = f"""
Combine these responses into one coherent answer.

Responses:
{json.dumps(results, indent=2)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text or ""
    saved_files: list[str] = []

    if docs_dir and file_prefix:
        saved_files = save_response_files(response, docs_dir, file_prefix)

        requested_file = detect_requested_file_type(user_prompt)
        if requested_file in FILE_GENERATORS:
            extension = f".{requested_file}"
            if (
                not _has_file_with_extension(results, extension)
                and not any(path.lower().endswith(extension) for path in saved_files)
            ):
                _, generated_path = FILE_GENERATORS[requested_file](
                    user_prompt,
                    docs_dir,
                    file_prefix,
                )
                saved_files.append(generated_path)
                label = FILE_LABELS.get(requested_file, "File")
                text = f"{text}\n\n{label} saved to: {generated_path}"

    return text, saved_files
