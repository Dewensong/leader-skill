from __future__ import annotations

from pathlib import Path


def extract_text_from_image(image_path: str | Path) -> dict[str, object]:
    path = Path(image_path)
    sidecar = path.with_suffix(".txt")
    if sidecar.exists():
        return {
            "text": sidecar.read_text(encoding="utf-8").strip(),
            "method": "sidecar",
            "warnings": [],
        }

    return {
        "text": "",
        "method": "unavailable",
        "warnings": [
            "OCR engine not configured. Add a same-name .txt sidecar file or install an OCR stack."
        ],
    }
