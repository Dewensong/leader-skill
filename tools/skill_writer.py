from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from tools.version_manager import snapshot_leader_state


def create_leader_instance(
    root: str | Path,
    slug: str,
    display_name: str,
    analyses: list[dict[str, object]],
    sources: list[dict[str, object]],
) -> Path:
    repo_root = Path(root)
    leader_dir = repo_root / "leaders" / slug
    leader_dir.mkdir(parents=True, exist_ok=True)
    (leader_dir / "versions").mkdir(exist_ok=True)

    persona_tags = Counter()
    for analysis in analyses:
        for tag in analysis.get("persona_tags", []):
            persona_tags[str(tag)] += 1

    top_tags = [tag for tag, _ in persona_tags.most_common(6)] or ["表达留白"]
    persona_body = "\n".join(f"- {tag}" for tag in top_tags)
    (leader_dir / "persona.md").write_text(
        "\n".join(
            [
                f"# {display_name} 画像",
                "",
                "## 领导标签",
                persona_body,
                "",
                "## 画像摘要",
                "这位领导偏好先把事情推进起来，再逐步校准细节，适合你提前准备边界问题和可评审版本。",
            ]
        ),
        encoding="utf-8",
    )

    intent_sections = []
    for index, analysis in enumerate(analyses, start=1):
        intent_sections.extend(
            [
                f"## 样本 {index}",
                f"- 原话：{analysis.get('original_text', analysis.get('source_label', '未知来源'))}",
                f"- 实际意思：{analysis.get('actual_meaning')}",
                f"- 优先级判断：{analysis.get('priority_signal')}",
                f"- 风险点：{'；'.join(analysis.get('risk_points', []))}",
                "",
            ]
        )
    (leader_dir / "intent-map.md").write_text(
        "# 意图地图\n\n" + "\n".join(intent_sections).strip() + "\n",
        encoding="utf-8",
    )

    playbook_sections = []
    for analysis in analyses:
        playbook_sections.extend(
            [
                f"## {analysis.get('source_label', '样本')}",
                f"- 推荐回复：{analysis.get('reply_suggestion')}",
                f"- 晋升打法：{analysis.get('promotion_hint')}",
                "",
            ]
        )
    (leader_dir / "playbook.md").write_text(
        "# 生存手册\n\n" + "\n".join(playbook_sections).strip() + "\n",
        encoding="utf-8",
    )

    (leader_dir / "sources.json").write_text(
        json.dumps(sources, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (leader_dir / "corrections.md").write_text(
        "# Corrections\n\n- 在这里记录“这句话他不会这么说”或“这位领导更看重时效/质量”的纠正。\n",
        encoding="utf-8",
    )

    snapshot_leader_state(leader_dir, note="initial generation")
    return leader_dir
