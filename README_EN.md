# leader-skill

`leader-skill` is a local-first boss-message decoder.

It translates vague manager requests into:

- actual meaning
- priority signal
- hidden risks
- safer replies
- upward-management moves

## Why it exists

Two meme-heavy open-source skills recently proved that simple ideas with sharp framing can travel very far:

- [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill)
- [therealXiaomanChu/ex-skill](https://github.com/therealXiaomanChu/ex-skill)

This project borrows the installable skill structure and local generation flow, but changes the product angle:

- not personality cosplay
- not a reskin
- instead: decode power language at work

## Core layers

- `Leader Persona`
- `Intent Map`
- `Survival Playbook`

## Example

```bash
python -m tools.cli translate --text "Could you quickly take a look and sync tomorrow?"
```

The output includes:

- actual meaning
- priority
- risk points
- suggested reply
- promotion hint

## Supported local sources

- pasted text
- screenshots
- Markdown / TXT
- PDF
- `.eml` / `.mbox`
- chat exports

## Install

```bash
git clone https://github.com/Dewensong/leader-skill.git
cd leader-skill
python -m pip install -r requirements.txt
```

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Safety

- local-first by default
- redact screenshots before sharing
- do not use it to harass, forge, or target real people
