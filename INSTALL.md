# Install Guide

## Option A: install as a Claude Code skill

Claude Code looks for skills under `.claude/skills/`.

Install into the current project:

```bash
mkdir -p .claude/skills
git clone https://github.com/Dewensong/leader-skill .claude/skills/create-leader
```

Or install globally:

```bash
git clone https://github.com/Dewensong/leader-skill ~/.claude/skills/create-leader
```

## Option B: run it as a local CLI

Requirements:

- Python 3.11+
- Git

Install:

```bash
git clone https://github.com/Dewensong/leader-skill.git
cd leader-skill
python -m pip install -r requirements.txt
```

## Verify the install

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Try the fastest demo:

```bash
python -m tools.cli translate --text "这个你先看一下，晚点我们再对齐。"
```

The default output is Markdown. If you want JSON for scripting:

```bash
python -m tools.cli translate --text "这个你先看一下，晚点我们再对齐。" --format json
```

## Create your first leader profile

```bash
python -m tools.cli create-leader \
  --slug pragmatic-lead \
  --name "务实型领导" \
  --text "这个不复杂吧，今天先出一个方案，明天同步一下。"
```

Then open the generated bundle:

```bash
python -m tools.cli show-leader --slug pragmatic-lead
```

If you are writing into a custom repo root, add `--root "D:\\path\\to\\repo-root"`.

## Import a screenshot

```bash
python -m tools.cli create-leader \
  --slug screenshot-boss \
  --name "截图型领导" \
  --input .\\samples\\boss-message.png
```

If OCR is not configured, place a same-name sidecar text file next to the image:

```text
boss-message.png
boss-message.txt
```

## Roll back a profile

```bash
python -m tools.cli leader-rollback --slug pragmatic-lead --version 20260401010101000000
```

## Recommended next read

- [README.md](./README.md)
- [docs/architecture.md](./docs/architecture.md)
- [examples/demo-leader/README.md](./examples/demo-leader/README.md)
