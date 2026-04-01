# Architecture

`leader-skill` is intentionally split into three product layers and a small local tooling layer.

## Product Layers

### Leader Persona

Captures how a leader tends to communicate:

- urgency style
- ambiguity tolerance
- decision habits
- preference for speed, polish, or visibility

### Intent Map

Maps recurring phrases to probable reality:

- actual meaning
- implied priority
- hidden risk
- likely delivery expectation

### Survival Playbook

Turns analysis into action:

- reply suggestion
- follow-up questions
- reporting strategy
- promotion-minded framing

## Local Tooling

- `analysis_engine.py`: phrase heuristics and score generation
- `source_router.py`: file-type dispatch
- `skill_writer.py`: writes generated leader artifacts
- `version_manager.py`: snapshots and rollbacks

The first release keeps everything local-first and file-based so it is easy to audit, hack, and extend.
