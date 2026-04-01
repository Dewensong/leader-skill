from __future__ import annotations

from typing import Iterable


def render_analysis_markdown(title: str, analysis: dict[str, object]) -> str:
    risk_points = analysis.get("risk_points", [])
    persona_tags = analysis.get("persona_tags", [])
    follow_up_questions = analysis.get("follow_up_questions", [])
    scores = analysis.get("scores", {})

    sections = [
        f"# {title}",
        "",
        "## 实际意思",
        str(analysis.get("actual_meaning", "")),
        "",
        "## 画像摘要",
        str(analysis.get("persona_summary", "")),
        "",
        "## 优先级判断",
        str(analysis.get("priority_signal", "")),
        "",
        "## 风险点",
    ]
    sections.extend(_to_bullets(risk_points))
    sections.extend(
        [
            "",
            "## 建议回复",
            str(analysis.get("reply_suggestion", "")),
            "",
            "## 建议追问",
        ]
    )
    sections.extend(_to_bullets(follow_up_questions))
    sections.extend(
        [
            "",
            "## 晋升打法",
            str(analysis.get("promotion_hint", "")),
            "",
            "## 领导标签",
        ]
    )
    sections.extend(_to_bullets(persona_tags))
    sections.extend(["", "## 指数分"])
    sections.extend(
        [
            f"- 甩锅风险：{scores.get('blame_risk', 0)}",
            f"- 范围膨胀：{scores.get('scope_creep', 0)}",
            f"- 今晚加班概率：{scores.get('overtime_probability', 0)}",
        ]
    )
    return "\n".join(sections).strip() + "\n"


def render_reply_markdown(analysis: dict[str, object], follow_up_questions: Iterable[str]) -> str:
    lines = [
        "# 建议回复",
        "",
        str(analysis.get("reply_suggestion", "")),
        "",
        "## 建议追问",
    ]
    lines.extend(_to_bullets(follow_up_questions))
    return "\n".join(lines).strip() + "\n"


def render_risk_markdown(analysis: dict[str, object]) -> str:
    scores = analysis.get("scores", {})
    lines = [
        "# 风险分析",
        "",
        "## 风险点",
    ]
    lines.extend(_to_bullets(analysis.get("risk_points", [])))
    lines.extend(
        [
            "",
            "## 指数分",
            f"- 甩锅风险：{scores.get('blame_risk', 0)}",
            f"- 范围膨胀：{scores.get('scope_creep', 0)}",
            f"- 今晚加班概率：{scores.get('overtime_probability', 0)}",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def render_promotion_markdown(analysis: dict[str, object], visibility_move: str) -> str:
    lines = [
        "# 向上管理建议",
        "",
        "## 晋升打法",
        str(analysis.get("promotion_hint", "")),
        "",
        "## 可见度动作",
        visibility_move,
    ]
    return "\n".join(lines).strip() + "\n"


def render_persona_markdown(analysis: dict[str, object]) -> str:
    lines = [
        "# 领导画像",
        "",
        "## 标签",
    ]
    lines.extend(_to_bullets(analysis.get("persona_tags", [])))
    lines.extend(
        [
            "",
            "## 画像摘要",
            str(analysis.get("persona_summary", "")),
        ]
    )
    return "\n".join(lines).strip() + "\n"


def render_priority_markdown(analysis: dict[str, object]) -> str:
    scores = analysis.get("scores", {})
    lines = [
        "# 优先级判断",
        "",
        str(analysis.get("priority_signal", "")),
        "",
        "## 指数分",
        f"- 甩锅风险：{scores.get('blame_risk', 0)}",
        f"- 范围膨胀：{scores.get('scope_creep', 0)}",
        f"- 今晚加班概率：{scores.get('overtime_probability', 0)}",
    ]
    return "\n".join(lines).strip() + "\n"


def render_leader_summary_markdown(
    slug: str,
    display_name: str,
    persona: str,
    intent_map: str,
    playbook: str,
) -> str:
    lines = [
        f"# {display_name}",
        "",
        f"> 实例 slug: `{slug}`",
        "",
        "## 画像",
        _demote_headings(_strip_top_heading(persona)),
        "",
        "## 意图地图",
        _demote_headings(_strip_top_heading(intent_map)),
        "",
        "## 生存手册",
        _demote_headings(_strip_top_heading(playbook)),
    ]
    return "\n".join(lines).strip() + "\n"


def _to_bullets(items: Iterable[object]) -> list[str]:
    values = [str(item) for item in items if str(item).strip()]
    if not values:
        return ["- 暂无"]
    return [f"- {value}" for value in values]


def _strip_top_heading(content: str) -> str:
    lines = content.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def _demote_headings(content: str) -> str:
    lines = []
    for line in content.splitlines():
        if line.startswith("### "):
            lines.append(f"#### {line[4:]}")
        elif line.startswith("## "):
            lines.append(f"### {line[3:]}")
        elif line.startswith("# "):
            lines.append(f"## {line[2:]}")
        else:
            lines.append(line)
    return "\n".join(lines).strip()
