# leader-skill

`leader-skill` is a local-first decoder for vague boss messages.

It turns messy workplace language into something actionable:

- actual meaning
- priority signal
- hidden risks
- safer replies
- upward-management moves

## What makes it interesting

This repository borrows the high-virality skill packaging style seen in:

- [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)
- [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill)

But the subject is different:

- not coworkers
- not ex-partners
- instead: leadership language at work

The goal is simple: make vague assignments less mysterious and less dangerous.

## Quick start

### Install as a Claude Code skill

```bash
mkdir -p .claude/skills
git clone https://github.com/Dewensong/leader-skill .claude/skills/create-leader
```

### Or run it locally

```bash
git clone https://github.com/Dewensong/leader-skill.git
cd leader-skill
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py"
```

Try the most common phrase:

```bash
python -m tools.cli translate --text "Please take a look first, and we can align later."
```

The CLI now defaults to human-readable Markdown. Use `--format json` if you want machine output.

## Supported sources

- pasted text
- screenshots
- Markdown / TXT
- PDF
- `.eml` / `.mbox`
- chat export JSON

Everything is designed to stay local-first by default.

## Sample bundle

If you want to inspect the output without running anything first:

- [examples/demo-leader/README.md](./examples/demo-leader/README.md)
- [examples/demo-leader/persona.md](./examples/demo-leader/persona.md)
- [examples/demo-leader/intent-map.md](./examples/demo-leader/intent-map.md)
- [examples/demo-leader/playbook.md](./examples/demo-leader/playbook.md)

## Core commands

- `python -m tools.cli create-leader`
- `python -m tools.cli list-leaders`
- `python -m tools.cli show-leader`
- `python -m tools.cli translate`
- `python -m tools.cli priority`
- `python -m tools.cli persona`
- `python -m tools.cli reply`
- `python -m tools.cli risk`
- `python -m tools.cli promotion`
- `python -m tools.cli leader-rollback`
- `python -m tools.cli delete-leader`

## Safety

- local-first by default
- redact screenshots before importing them
- do not use it to harass, forge, monitor, or target real people
- the point is clearer communication, not manipulative behavior
