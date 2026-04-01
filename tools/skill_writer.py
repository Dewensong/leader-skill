from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from tools.version_manager import snapshot_leader_state


def _average_scores(analyses: list[dict[str, object]]) -> dict[str, int]:
    score_keys = ("blame_risk", "scope_creep", "overtime_probability")
    averages: dict[str, int] = {}
    for key in score_keys:
        values = [
            int(analysis.get("scores", {}).get(key, 0))
            for analysis in analyses
            if isinstance(analysis.get("scores", {}), dict)
        ]
        averages[key] = round(sum(values) / len(values)) if values else 0
    return averages


def _bundle_summary(top_tags: list[str], average_scores: dict[str, int]) -> str:
    bits: list[str] = []
    tag_set = set(top_tags)
    if "时间预期偏紧" in tag_set or average_scores["overtime_probability"] >= 60:
        bits.append("推进节奏偏快")
    if "会前补需求" in tag_set or "默认先给初稿" in tag_set:
        bits.append("习惯先推进再补边界")
    if "口径敏感" in tag_set:
        bits.append("对同步口径比较敏感")
    if "责任边界模糊" in tag_set or average_scores["blame_risk"] >= 65:
        bits.append("需要你主动把责任边界写清楚")
    if not bits:
        bits.append("表达留白较多，需要你主动补全目标和验收标准")
    return "；".join(bits) + "。"


def _communication_moves(top_tags: list[str], average_scores: dict[str, int]) -> list[str]:
    moves = [
        "先给一版可评审产物，再在同步时锁定范围、优先级和验收标准。",
        "把临时任务改写成书面里程碑，让口头安排变成可追踪清单。",
    ]
    tag_set = set(top_tags)
    if "口径敏感" in tag_set:
        moves.append("同步前先准备一句结论版口径，避免会上被动改口。")
    elif average_scores["blame_risk"] >= 65:
        moves.append("关键节点用一句书面确认收口，降低后续“我以为你知道”的追责风险。")
    else:
        moves.append("每次反馈都先讲结果和影响，再讲执行细节，提升你的可见度。")
    return moves


def _collect_common_risks(analyses: list[dict[str, object]]) -> list[str]:
    risks: list[str] = []
    seen: set[str] = set()
    for analysis in analyses:
        for risk in analysis.get("risk_points", []):
            risk_text = str(risk).strip()
            if risk_text and risk_text not in seen:
                risks.append(risk_text)
                seen.add(risk_text)
            if len(risks) == 4:
                return risks
    return risks


def _pick_follow_up_questions(analyses: list[dict[str, object]]) -> list[str]:
    for analysis in analyses:
        questions = [str(item).strip() for item in analysis.get("follow_up_questions", []) if str(item).strip()]
        if questions:
            return questions[:3]
    return [
        "这件事的截止时间是今天、明天，还是本周内？",
        "你更希望先看到方案、结论，还是任务拆解？",
        "验收标准和优先级要不要我先写一版供你确认？",
    ]


def _render_bundle_readme(
    display_name: str,
    top_tags: list[str],
    bundle_summary: str,
    average_scores: dict[str, int],
    communication_moves: list[str],
) -> str:
    tag_text = " / ".join(top_tags) if top_tags else "表达留白"
    return "\n".join(
        [
            f"# {display_name}",
            "",
            "> 一个可直接打开查看的领导画像 bundle。先看标签和分数，再看意图地图和生存手册。",
            "",
            "## 快速速览",
            "",
            "| 维度 | 结论 |",
            "|---|---|",
            f"| 风格判断 | {bundle_summary} |",
            f"| 高频标签 | {tag_text} |",
            f"| 甩锅风险 | {average_scores['blame_risk']} |",
            f"| 范围膨胀 | {average_scores['scope_creep']} |",
            f"| 今晚加班概率 | {average_scores['overtime_probability']} |",
            "",
            "## 推荐打开顺序",
            "",
            "1. `persona.md`",
            "2. `intent-map.md`",
            "3. `playbook.md`",
            "4. `versions/`",
            "",
            "## 最值得先记住的 3 个动作",
            "",
            *(f"- {move}" for move in communication_moves),
            "",
            "## 为什么这个 bundle 有用",
            "",
            "- 它不是吐槽合集，而是把模糊话术翻译成可执行动作。",
            "- 它适合在开会前 30 秒快速预判风险和回复方式。",
            "- 它保留版本快照，方便你做增量修正而不是每次重来。",
        ]
    ) + "\n"


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
    average_scores = _average_scores(analyses)
    bundle_summary = _bundle_summary(top_tags, average_scores)
    communication_moves = _communication_moves(top_tags, average_scores)
    common_risks = _collect_common_risks(analyses)
    common_risk_lines = [f"- {risk}" for risk in common_risks] if common_risks else ["- 暂无"]
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
                bundle_summary,
                "",
                "## 沟通策略",
                *[f"- {move}" for move in communication_moves],
                "",
                "## 风险体感",
                f"- 甩锅风险：{average_scores['blame_risk']}",
                f"- 范围膨胀：{average_scores['scope_creep']}",
                f"- 今晚加班概率：{average_scores['overtime_probability']}",
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
                f"- 指数分：甩锅 {analysis.get('scores', {}).get('blame_risk', 0)} / 范围 {analysis.get('scores', {}).get('scope_creep', 0)} / 加班 {analysis.get('scores', {}).get('overtime_probability', 0)}",
                "",
            ]
        )
    (leader_dir / "intent-map.md").write_text(
        "# 意图地图\n\n" + "\n".join(intent_sections).strip() + "\n",
        encoding="utf-8",
    )

    default_questions = _pick_follow_up_questions(analyses)
    playbook_sections = []
    playbook_sections.extend(
        [
            "## 默认动作",
            "- 先给可评审版本，再把范围、优先级和验收标准补成书面。",
            "- 同步前先整理一句结论版口径，避免临场被动。",
            "- 关键节点主动暴露风险和取舍，提升可见度而不是只报进度。",
            "",
            "## 默认追问",
            *[f"- {question}" for question in default_questions],
            "",
            "## 共性雷区",
            *common_risk_lines,
            "",
        ]
    )
    for analysis in analyses:
        questions = [str(item).strip() for item in analysis.get("follow_up_questions", []) if str(item).strip()] or default_questions
        playbook_sections.extend(
            [
                f"## {analysis.get('source_label', '样本')}",
                f"- 推荐回复：{analysis.get('reply_suggestion')}",
                f"- 建议追问：{'；'.join(questions)}",
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
    (leader_dir / "README.md").write_text(
        _render_bundle_readme(
            display_name=display_name,
            top_tags=top_tags,
            bundle_summary=bundle_summary,
            average_scores=average_scores,
            communication_moves=communication_moves,
        ),
        encoding="utf-8",
    )

    snapshot_leader_state(leader_dir, note="initial generation")
    return leader_dir
