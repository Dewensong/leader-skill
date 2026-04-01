from __future__ import annotations

from pathlib import Path


def parse_document(path: str | Path) -> dict[str, object]:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return {
            "text": file_path.read_text(encoding="utf-8"),
            "type": "document",
            "method": "plain-text",
        }

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore
        except ImportError:
            return {
                "text": "",
                "type": "document",
                "method": "pdf-unavailable",
                "warnings": ["Install pypdf to enable PDF text extraction."],
            }

        reader = PdfReader(str(file_path))
        content = "\n".join(page.extract_text() or "" for page in reader.pages)
        return {
            "text": content.strip(),
            "type": "document",
            "method": "pypdf",
        }

    raise ValueError(f"Unsupported document type: {file_path.suffix}")
