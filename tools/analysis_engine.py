from __future__ import annotations

import re
from typing import Iterable


def _cap_score(value: int) -> int:
    return max(0, min(100, value))


def _build_reply(text: str, cues: set[str]) -> str:
    if "soft_review" in cues and "alignment" in cues:
        return "我先整理一版可评审内容，今晚给你初稿，明天同步时一起确认范围、优先级和验收标准。"
    if "underspecified_scope" in cues:
        return "我先按当前理解出一版方案，同时把目标、范围和验收标准列清楚，避免明天同步时信息缺口。"
    if "flexible_blame" in cues:
        return "我先按两个方案整理利弊，同时把目标、时间和责任边界写清楚，方便你拍板。"
    if "quick_peek" in cues:
        return "我先快速过一遍，稍后把关键风险、时间预估和需要你确认的点同步给你。"
    return f"我先按当前理解推进，并把目标、范围、时间预期整理清楚后再和你确认。原话：{text}"


def _build_promotion_hint(tags: Iterable[str]) -> str:
    tag_set = set(tags)
    if "愿景管理" in tag_set:
        return "汇报时先讲结果和影响，再补执行路径，让领导更容易把你和业务推进绑定在一起。"
    if "责任边界模糊" in tag_set:
        return "每次同步都留下一句书面确认，把目标、截止时间和验收标准写清楚，能显著降低背锅概率。"
    return "把每次临时任务都沉淀成可追踪的结果清单，持续积累可见度和可归因的贡献。"


def _build_follow_up_questions(cues: set[str]) -> list[str]:
    questions: list[str] = []
    if "soft_review" in cues or "underspecified_scope" in cues:
        questions.append("你更希望我先给方案、结论，还是一版可直接评审的初稿？")
    if "alignment" in cues:
        questions.append("这次同步最需要对齐的是方向、范围，还是口径和优先级？")
    if "flexible_blame" in cues:
        questions.append("这件事里哪些边界需要你拍板，哪些我可以直接推进？")
    if "quick_peek" in cues:
        questions.append("你希望我先同步关键风险，还是直接给一版可讨论的内容？")
    if "underspecified_scope" in cues:
        questions.append("验收标准和截止时间，我要不要先整理成书面版给你确认？")

    defaults = [
        "这件事的截止时间是今天、明天，还是本周内？",
        "你更希望先看到方案、结论，还是任务拆解？",
        "验收标准和优先级要不要我先写一版供你确认？",
    ]
    for question in defaults:
        questions.append(question)

    deduped: list[str] = []
    seen: set[str] = set()
    for question in questions:
        if question not in seen:
            deduped.append(question)
            seen.add(question)
        if len(deduped) == 3:
            break
    return deduped


def _build_persona_summary(tags: Iterable[str], scores: dict[str, int]) -> str:
    tag_set = set(tags)
    summary_bits: list[str] = []

    if "时间预期偏紧" in tag_set or scores.get("overtime_probability", 0) >= 60:
        summary_bits.append("推进节奏偏快，默认你会先垫出一版")
    if "会前补需求" in tag_set or "默认先给初稿" in tag_set:
        summary_bits.append("习惯先推进再补边界")
    if "口径敏感" in tag_set:
        summary_bits.append("同步时会在意口径是否一致")
    if "责任边界模糊" in tag_set or scores.get("blame_risk", 0) >= 65:
        summary_bits.append("需要你主动用书面方式锁定责任和验收标准")

    if not summary_bits:
        summary_bits.append("表达留白较多，需要你主动补齐目标、边界和节奏")

    return "；".join(summary_bits) + "。"


def analyze_message(message: str) -> dict[str, object]:
    text = re.sub(r"\s+", " ", message).strip()
    actual_bits: list[str] = []
    risk_points: list[str] = []
    persona_tags: set[str] = set()
    cues: set[str] = set()
    scores = {
        "blame_risk": 35,
        "scope_creep": 35,
        "overtime_probability": 35,
    }

    if "先看一下" in text or "看一下" in text:
        actual_bits.append("这不是简单看看，而是希望你尽快形成反馈、判断或可评审产出。")
        risk_points.append("优先级没有被明确写出来，容易打乱你当前排期。")
        persona_tags.update({"口头优先级偏高", "愿景管理"})
        cues.update({"soft_review", "quick_peek"})
        scores["overtime_probability"] += 25
        scores["scope_creep"] += 15

    if "对齐" in text:
        actual_bits.append("所谓再对齐，通常意味着你需要带着方案去确认边界、责任和口径。")
        risk_points.append("优先级和验收标准可能还没有真正定清。")
        persona_tags.update({"会前补需求", "口径敏感"})
        cues.add("alignment")
        scores["blame_risk"] += 10
        scores["scope_creep"] += 10

    if "不复杂" in text or "简单" in text:
        actual_bits.append("需求还没完全定义，但对方默认你会快速交出第一版。")
        risk_points.append("验收标准仍然模糊，后续容易出现范围膨胀。")
        persona_tags.update({"压缩工期", "默认先给初稿"})
        cues.add("underspecified_scope")
        scores["blame_risk"] += 20
        scores["scope_creep"] += 25
        scores["overtime_probability"] += 15

    if "灵活处理" in text or "你看着办" in text:
        actual_bits.append("领导暂时不想明确拍板，但结果仍然希望由你兜住。")
        risk_points.append("责任边界模糊，后续容易出现“我以为你知道”的追责场景。")
        persona_tags.update({"责任边界模糊", "放权但保留追责权"})
        cues.add("flexible_blame")
        scores["blame_risk"] += 30
        scores["scope_creep"] += 10

    if "今天" in text or "今晚" in text:
        persona_tags.add("时间预期偏紧")
        scores["overtime_probability"] += 20

    if "明天" in text or "同步一下" in text:
        risk_points.append("同步节点很近，说明至少需要一版能拿出来讨论的内容。")
        scores["blame_risk"] += 15

    if not actual_bits:
        actual_bits.append("语气看似松弛，但需要你主动把目标、优先级和交付边界问清楚。")
        risk_points.append("没有明确验收标准时，最好主动补一轮问题确认。")
        persona_tags.add("表达留白")

    priority_signal = "高优先级，建议当天给到初版或明确阻塞。"
    if scores["overtime_probability"] < 55 and scores["blame_risk"] < 55:
        priority_signal = "中优先级，建议先确认预期结果和截止时间，再决定是否插队。"

    result = {
        "source_label": "inline-text",
        "original_text": text,
        "actual_meaning": " ".join(actual_bits),
        "priority_signal": priority_signal,
        "risk_points": risk_points,
        "reply_suggestion": _build_reply(text, cues),
        "promotion_hint": _build_promotion_hint(persona_tags),
        "follow_up_questions": _build_follow_up_questions(cues),
        "persona_summary": _build_persona_summary(persona_tags, {key: _cap_score(value) for key, value in scores.items()}),
        "persona_tags": sorted(persona_tags),
        "scores": {key: _cap_score(value) for key, value in scores.items()},
    }
    return result
