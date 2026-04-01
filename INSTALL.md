# Install Guide

## Requirements

- Python 3.11+
- Git

Optional for richer parsing:

- `pypdf`
- `Pillow`
- `pytesseract`
- system OCR runtime if you want real image OCR instead of sidecar `.txt`

## Local Setup

```bash
git clone https://github.com/Dewensong/leader-skill.git
cd leader-skill
python -m pip install -r requirements.txt
```

## Quick Smoke Test

```bash
python -m tools.cli translate --text "这个你先看一下，晚点我们再对齐。"
python -m unittest discover -s tests -p "test_*.py"
```

## Create a Leader Profile

```bash
python -m tools.cli create-leader \
  --slug pragmatic-lead \
  --name "务实型负责人" \
  --text "这个不复杂吧，你今天先出个方案。"
```

## Import Files

```bash
python -m tools.cli create-leader \
  --slug screenshot-boss \
  --name "截图型领导" \
  --input .\\samples\\boss-message.png
```

If real OCR is not configured yet, add a same-name sidecar text file:

```text
boss-message.png
boss-message.txt
```

## Roll Back a Profile

```bash
python -m tools.cli leader-rollback --slug pragmatic-lead --version 20260401010101000000
```
