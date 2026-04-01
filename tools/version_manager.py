from __future__ import annotations

import json
import shutil
from datetime import datetime, UTC
from pathlib import Path


CORE_FILES = [
    "persona.md",
    "intent-map.md",
    "playbook.md",
    "sources.json",
    "corrections.md",
]


def snapshot_leader_state(leader_dir: str | Path, note: str = "") -> str:
    target = Path(leader_dir)
    versions_dir = target / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)

    version_id = datetime.now(UTC).strftime("%Y%m%d%H%M%S%f")
    version_dir = versions_dir / version_id
    version_dir.mkdir(parents=True, exist_ok=False)

    for name in CORE_FILES:
        source = target / name
        if source.exists():
            shutil.copy2(source, version_dir / name)

    metadata = {
        "version_id": version_id,
        "note": note,
        "created_at": datetime.now(UTC).isoformat(),
    }
    (version_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return version_id


def restore_version(leader_dir: str | Path, version_id: str) -> None:
    target = Path(leader_dir)
    version_dir = target / "versions" / version_id
    if not version_dir.exists():
        raise FileNotFoundError(f"Unknown version: {version_id}")

    for name in CORE_FILES:
        source = version_dir / name
        if source.exists():
            shutil.copy2(source, target / name)
