from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from tools.analysis_engine import analyze_message
from tools.report_formatter import (
    render_analysis_markdown,
    render_leader_summary_markdown,
    render_persona_markdown,
    render_priority_markdown,
    render_promotion_markdown,
    render_reply_markdown,
    render_risk_markdown,
)
from tools.skill_writer import create_leader_instance
from tools.source_router import load_source
from tools.version_manager import restore_version


def repo_root_from_arg(value: str | None) -> Path:
    if value:
        return Path(value).resolve()
    return Path(__file__).resolve().parents[1]


def cmd_create_leader(args: argparse.Namespace) -> int:
    root = repo_root_from_arg(args.root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "leaders").mkdir(exist_ok=True)

    sources: list[dict[str, object]] = []
    analyses: list[dict[str, object]] = []

    if args.text:
        analysis = analyze_message(args.text)
        analysis["source_label"] = "inline-text"
        sources.append(
            {
                "type": "text",
                "label": "inline-text",
                "preview": args.text[:120],
            }
        )
        analyses.append(analysis)

    for input_path in args.input or []:
        source = load_source(input_path)
        text = str(source.get("text", "")).strip() or str(source.get("preview", "")).strip()
        analysis = analyze_message(text)
        analysis["source_label"] = str(source.get("label", "file-source"))
        analysis["original_text"] = text
        analyses.append(analysis)
        sources.append(
            {
                key: value
                for key, value in source.items()
                if key in {"type", "label", "preview", "method", "path", "warnings"}
            }
        )

    if not analyses:
        raise SystemExit("At least one --text or --input value is required.")

    output_dir = create_leader_instance(
        root=root,
        slug=args.slug,
        display_name=args.name,
        analyses=analyses,
        sources=sources,
    )

    response = {
        "slug": args.slug,
        "name": args.name,
        "leader_dir": str(output_dir),
        "source_count": len(sources),
    }
    print(json.dumps(response, ensure_ascii=False, indent=2))
    return 0


def _load_leader_summary(root: Path, slug: str) -> dict[str, object]:
    leader_dir = root / "leaders" / slug
    if not leader_dir.exists():
        raise FileNotFoundError(f"Leader not found: {slug}")
    persona_text = (leader_dir / "persona.md").read_text(encoding="utf-8")
    first_heading = next(
        (line.strip().removeprefix("# ").replace(" 画像", "") for line in persona_text.splitlines() if line.startswith("# ")),
        slug,
    )
    return {
        "slug": slug,
        "leader_dir": str(leader_dir),
        "display_name": first_heading,
        "persona": persona_text,
        "intent_map": (leader_dir / "intent-map.md").read_text(encoding="utf-8"),
        "playbook": (leader_dir / "playbook.md").read_text(encoding="utf-8"),
    }


def cmd_list_leaders(args: argparse.Namespace) -> int:
    root = repo_root_from_arg(args.root)
    leaders_dir = root / "leaders"
    items = []
    if leaders_dir.exists():
        for child in sorted(leaders_dir.iterdir()):
            if child.is_dir() and (child / "persona.md").exists():
                items.append({"slug": child.name, "path": str(child)})
    print(json.dumps(items, ensure_ascii=False, indent=2))
    return 0


def cmd_show_leader(args: argparse.Namespace) -> int:
    root = repo_root_from_arg(args.root)
    summary = _load_leader_summary(root, args.slug)
    if args.format == "markdown":
        print(
            render_leader_summary_markdown(
                slug=str(summary["slug"]),
                display_name=str(summary["display_name"]),
                persona=str(summary["persona"]),
                intent_map=str(summary["intent_map"]),
                playbook=str(summary["playbook"]),
            ),
            end="",
        )
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def cmd_translate(args: argparse.Namespace) -> int:
    analysis = analyze_message(args.text)
    if args.format == "markdown":
        print(render_analysis_markdown("领导黑话翻译", analysis), end="")
    else:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    return 0


def cmd_priority(args: argparse.Namespace) -> int:
    analysis = analyze_message(args.text)
    payload = {
        "priority_signal": analysis["priority_signal"],
        "scores": analysis["scores"],
    }
    if args.format == "markdown":
        print(render_priority_markdown(analysis), end="")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_persona(args: argparse.Namespace) -> int:
    analysis = analyze_message(args.text)
    payload = {
        "persona_tags": analysis["persona_tags"],
        "persona_summary": analysis["persona_summary"],
        "promotion_hint": analysis["promotion_hint"],
    }
    if args.format == "markdown":
        print(render_persona_markdown(analysis), end="")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_reply(args: argparse.Namespace) -> int:
    analysis = analyze_message(args.text)
    follow_up_questions = analysis["follow_up_questions"]
    payload = {
        "reply_suggestion": analysis["reply_suggestion"],
        "follow_up_questions": follow_up_questions,
    }
    if args.format == "markdown":
        print(render_reply_markdown(analysis, follow_up_questions), end="")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_risk(args: argparse.Namespace) -> int:
    analysis = analyze_message(args.text)
    payload = {
        "risk_points": analysis["risk_points"],
        "scores": analysis["scores"],
    }
    if args.format == "markdown":
        print(render_risk_markdown(analysis), end="")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_promotion(args: argparse.Namespace) -> int:
    analysis = analyze_message(args.text)
    visibility_move = "把本次任务拆成书面里程碑，并在同步时主动复盘你提前识别的风险与取舍。"
    payload = {
        "promotion_hint": analysis["promotion_hint"],
        "visibility_move": visibility_move,
    }
    if args.format == "markdown":
        print(render_promotion_markdown(analysis, visibility_move), end="")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_leader_rollback(args: argparse.Namespace) -> int:
    root = repo_root_from_arg(args.root)
    restore_version(root / "leaders" / args.slug, args.version)
    print(json.dumps({"slug": args.slug, "restored_version": args.version}, ensure_ascii=False, indent=2))
    return 0


def cmd_delete_leader(args: argparse.Namespace) -> int:
    root = repo_root_from_arg(args.root)
    leader_dir = root / "leaders" / args.slug
    if not args.yes:
        raise SystemExit("Refusing to delete without --yes.")
    shutil.rmtree(leader_dir)
    print(json.dumps({"deleted": args.slug}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="leader-skill")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create-leader")
    create.add_argument("--root")
    create.add_argument("--slug", required=True)
    create.add_argument("--name", required=True)
    create.add_argument("--text")
    create.add_argument("--input", action="append")
    create.set_defaults(func=cmd_create_leader)

    listing = subparsers.add_parser("list-leaders")
    listing.add_argument("--root")
    listing.set_defaults(func=cmd_list_leaders)

    show = subparsers.add_parser("show-leader")
    show.add_argument("--root")
    show.add_argument("--slug", required=True)
    show.add_argument("--format", choices=["json", "markdown"], default="markdown")
    show.set_defaults(func=cmd_show_leader)

    translate = subparsers.add_parser("translate")
    translate.add_argument("--text", required=True)
    translate.add_argument("--format", choices=["json", "markdown"], default="markdown")
    translate.set_defaults(func=cmd_translate)

    priority = subparsers.add_parser("priority")
    priority.add_argument("--text", required=True)
    priority.add_argument("--format", choices=["json", "markdown"], default="markdown")
    priority.set_defaults(func=cmd_priority)

    persona = subparsers.add_parser("persona")
    persona.add_argument("--text", required=True)
    persona.add_argument("--format", choices=["json", "markdown"], default="markdown")
    persona.set_defaults(func=cmd_persona)

    reply = subparsers.add_parser("reply")
    reply.add_argument("--text", required=True)
    reply.add_argument("--format", choices=["json", "markdown"], default="markdown")
    reply.set_defaults(func=cmd_reply)

    risk = subparsers.add_parser("risk")
    risk.add_argument("--text", required=True)
    risk.add_argument("--format", choices=["json", "markdown"], default="markdown")
    risk.set_defaults(func=cmd_risk)

    promotion = subparsers.add_parser("promotion")
    promotion.add_argument("--text", required=True)
    promotion.add_argument("--format", choices=["json", "markdown"], default="markdown")
    promotion.set_defaults(func=cmd_promotion)

    rollback = subparsers.add_parser("leader-rollback")
    rollback.add_argument("--root")
    rollback.add_argument("--slug", required=True)
    rollback.add_argument("--version", required=True)
    rollback.set_defaults(func=cmd_leader_rollback)

    delete = subparsers.add_parser("delete-leader")
    delete.add_argument("--root")
    delete.add_argument("--slug", required=True)
    delete.add_argument("--yes", action="store_true")
    delete.set_defaults(func=cmd_delete_leader)

    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
