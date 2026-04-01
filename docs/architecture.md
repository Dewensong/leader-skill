# Architecture

`leader-skill` is intentionally small, local-first, and easy to audit.

## System shape

```text
input -> normalize -> analyze -> write -> version -> present
```

## Product layers

### Leader Persona

Turn repeated phrases into a recognizable management style:

- urgency preference
- ambiguity tolerance
- decision habits
- sensitivity to scope, timing, and public alignment

### Intent Map

Turn specific phrases into likely intent:

- actual meaning
- implied priority
- hidden risk
- expected delivery shape

### Survival Playbook

Turn analysis into action:

- safer replies
- follow-up questions
- reporting moves
- promotion-minded visibility tactics

## Local tooling responsibilities

- `source_router`: route inputs by file type
- `document_parser`: read local text, Markdown, PDF, and exports
- `image_ocr`: extract text from screenshots with sidecar fallback
- `analysis_engine`: derive meaning, risk, tags, follow-up questions, and score signals
- `skill_writer`: write a complete leader bundle plus a human-friendly bundle README
- `version_manager`: snapshot and restore bundle history
- `report_formatter`: render Markdown-first terminal output for humans

## Output contract

Every generated leader bundle should keep a stable shape:

- `README.md`
- `persona.md`
- `intent-map.md`
- `playbook.md`
- `sources.json`
- `corrections.md`
- `versions/`

That makes the repository easier to trust:

- humans can open one bundle and understand it quickly
- contributors can diff changes cleanly
- future parsers can keep writing to a predictable contract
