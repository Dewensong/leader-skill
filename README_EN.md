# leader.skill

> "This is simple. Please handle it today. The boss wants to see it tomorrow. We can align on details later."

`leader-skill` is a local-first decoder for boss language.

It is heavily inspired by the packaging style of:

- [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)
- [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill)

But the target is different: not coworkers, not ex-partners, but leaders and managers.

## What it does

It turns vague workplace phrases into:

- actual meaning
- priority judgment
- hidden risk
- safer reply suggestions
- upward-management moves

## Install

### Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/Dewensong/leader-skill .claude/skills/create-leader
```

### Local CLI

```bash
git clone https://github.com/Dewensong/leader-skill.git
cd leader-skill
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py"
```

## Quick use

```bash
python -m tools.cli translate --text "Please take a look first, and we can align later."
```

The CLI defaults to human-readable Markdown. Use `--format json` when you want machine output.

## Supported sources

| Source | Status | Notes |
| --- | --- | --- |
| pasted text | supported | best for quick testing |
| screenshots | supported | OCR sidecar workflow |
| Markdown / TXT | supported | meeting notes, exports |
| PDF | supported | attachments, docs |
| `.eml` / `.mbox` | supported | email archives |
| chat export JSON | supported | local exports |
| online Feishu / DingTalk collection | planned | not required for v1 |

## Example scenarios

### "Please take a look first"

```text
User          ❯ Help me decode: please take a look first, and we can align later.

leader.skill  ❯ This does not mean “look when you have time”
               It usually means “prepare something reviewable first”
               Better assume a draft is needed before the sync
```

### "This should be simple"

```text
User          ❯ My manager said: this should be simple, give me a plan today.

leader.skill  ❯ “Simple” often does not mean easy
               It often means the scope is still fuzzy but you are expected to move first
               Clarify scope before you over-commit
```

## Bundle structure

Each generated leader profile includes:

- `README.md`
- `persona.md`
- `intent-map.md`
- `playbook.md`
- `sources.json`
- `corrections.md`
- `versions/`

## Safety

- local-first by default
- redact screenshots before import
- do not use it to harass, forge, monitor, or target real people
- the goal is clearer communication, not manipulative behavior
