from __future__ import annotations

import json
from pathlib import Path


def parse_chat_export(path: str | Path) -> dict[str, object]:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix == ".txt":
        return {
            "text": file_path.read_text(encoding="utf-8"),
            "type": "chat-export",
            "method": "plain-text",
        }

    if suffix == ".json":
        data = json.loads(file_path.read_text(encoding="utf-8"))
        messages: list[str] = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    speaker = item.get("speaker") or item.get("role") or "unknown"
                    content = item.get("content") or item.get("text") or ""
                    messages.append(f"{speaker}: {content}")
        elif isinstance(data, dict) and isinstance(data.get("messages"), list):
            for item in data["messages"]:
                if isinstance(item, dict):
                    speaker = item.get("speaker") or item.get("role") or "unknown"
                    content = item.get("content") or item.get("text") or ""
                    messages.append(f"{speaker}: {content}")
        return {
            "text": "\n".join(messages).strip(),
            "type": "chat-export",
            "method": "json",
        }

    raise ValueError(f"Unsupported chat export type: {file_path.suffix}")
