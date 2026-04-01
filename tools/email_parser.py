from __future__ import annotations

import mailbox
from email import policy
from email.parser import BytesParser
from pathlib import Path


def parse_email_export(path: str | Path) -> dict[str, object]:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix == ".eml":
        message = BytesParser(policy=policy.default).parsebytes(file_path.read_bytes())
        text = _extract_message_body(message)
        return {
            "text": text,
            "type": "email",
            "method": "eml",
        }

    if suffix == ".mbox":
        box = mailbox.mbox(file_path)
        parts: list[str] = []
        for message in box:
            subject = message.get("subject", "(no subject)")
            parts.append(f"Subject: {subject}\n{_extract_message_body(message)}")
        return {
            "text": "\n\n".join(parts).strip(),
            "type": "email",
            "method": "mbox",
        }

    raise ValueError(f"Unsupported email export type: {file_path.suffix}")


def _extract_message_body(message) -> str:
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                return part.get_content().strip()
        return ""
    payload = message.get_payload(decode=True)
    if isinstance(payload, bytes):
        charset = message.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="replace").strip()
    return str(payload).strip()
