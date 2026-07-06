import mimetypes
import re
from pathlib import Path

from config.gemini_client import client

MIME_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/ogg": ".ogg",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    "application/pdf": ".pdf",
    "application/json": ".json",
    "text/plain": ".txt",
    "text/csv": ".csv",
    "text/html": ".html",
    "application/zip": ".zip",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/msword": ".doc",
}


def extension_for_mime(mime_type: str | None) -> str:
    if not mime_type:
        return ".bin"

    mime_type = mime_type.split(";")[0].strip().lower()
    if mime_type in MIME_EXTENSIONS:
        return MIME_EXTENSIONS[mime_type]

    guessed = mimetypes.guess_extension(mime_type)
    return guessed or ".bin"


def _sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", name.strip())
    return cleaned or "file"


def _iter_parts(parts):
    if not parts:
        return

    for part in parts:
        if part.inline_data and part.inline_data.data:
            yield {
                "kind": "inline",
                "data": part.inline_data.data,
                "mime_type": part.inline_data.mime_type,
                "display_name": part.inline_data.display_name,
            }

        if part.file_data and part.file_data.file_uri:
            yield {
                "kind": "uri",
                "file_uri": part.file_data.file_uri,
                "mime_type": part.file_data.mime_type,
                "display_name": part.file_data.display_name,
            }

        if part.function_response and part.function_response.parts:
            yield from _iter_parts(part.function_response.parts)


def save_response_files(response, docs_dir: Path, prefix: str) -> list[str]:
    """Save all file parts from a GenAI response to Docs. Returns saved paths."""
    parts = response.parts
    if not parts:
        return []

    docs_dir.mkdir(exist_ok=True)
    saved_paths: list[str] = []
    file_index = 0

    for item in _iter_parts(parts):
        mime_type = item.get("mime_type")
        display_name = item.get("display_name")

        if item["kind"] == "inline":
            data = item["data"]
        else:
            try:
                data = client.files.download(file=item["file_uri"])
            except Exception:
                continue

        if display_name:
            filename = f"{prefix}_{_sanitize_filename(display_name)}"
            if not Path(filename).suffix:
                filename += extension_for_mime(mime_type)
        else:
            filename = f"{prefix}_{file_index}{extension_for_mime(mime_type)}"
            file_index += 1

        file_path = docs_dir / filename
        file_path.write_bytes(data)
        saved_paths.append(str(file_path.resolve()))

    return saved_paths
