from __future__ import annotations

from pathlib import Path

from tools.chat_export_parser import parse_chat_export
from tools.document_parser import parse_document
from tools.email_parser import parse_email_export
from tools.image_ocr import extract_text_from_image


def load_source(path: str | Path) -> dict[str, object]:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        payload = extract_text_from_image(file_path)
        return {
            "type": "image",
            "label": file_path.name,
            "preview": (payload.get("text") or "")[:120],
            "text": payload.get("text", ""),
            "method": payload.get("method"),
            "warnings": payload.get("warnings", []),
            "path": str(file_path),
        }

    if suffix in {".txt", ".md", ".pdf"}:
        payload = parse_document(file_path)
        return {
            "type": "document",
            "label": file_path.name,
            "preview": str(payload.get("text", ""))[:120],
            "text": payload.get("text", ""),
            "method": payload.get("method"),
            "path": str(file_path),
            "warnings": payload.get("warnings", []),
        }

    if suffix in {".json"}:
        payload = parse_chat_export(file_path)
        return {
            "type": "chat-export",
            "label": file_path.name,
            "preview": str(payload.get("text", ""))[:120],
            "text": payload.get("text", ""),
            "method": payload.get("method"),
            "path": str(file_path),
        }

    if suffix in {".eml", ".mbox"}:
        payload = parse_email_export(file_path)
        return {
            "type": "email",
            "label": file_path.name,
            "preview": str(payload.get("text", ""))[:120],
            "text": payload.get("text", ""),
            "method": payload.get("method"),
            "path": str(file_path),
        }

    raise ValueError(f"Unsupported source file: {file_path}")
