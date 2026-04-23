# Learning Project Tutor

Learning Project Tutor is a distributable agent skill and starter workspace for source-based 1:1 tutoring.

It maintains a topic workspace with source material, course maps, lessons, learner responses, diagnoses, optional bridge or reframe lessons, QA logs, memory files, and final transfer tasks. The teaching path is controlled by the learner's demonstrated understanding rather than by a fixed syllabus.

## Repository Contents

- `skill/`: installable agent skill with `SKILL.md`, platform adapters, templates, scripts, and reference rules.
- `starter-workspace/`: copyable workspace template with topic skeletons, memory files, helper tools, and a demo topic.
- `scripts/release.sh`: release archive builder.
- `VERSION`: current package version.
- `CHANGELOG.md`: version history.

## Workspace Model

Each topic contains:
- `00-source.md`: source material
- `00-course-map.md`: source-aware course plan
- `topic_state.yaml`: state control file
- `lessons/`: generated lessons
- `responses/`: learner responses
- `diagnosis/`: teaching diagnoses
- `final/`: synthesis, transfer, articulation, and closure files
- `memory/`: topic-level memory context
- `qa/`: lesson QA log when needed

Supported platform adapters:
- `codex`: `AGENTS.md`
- `claude-code`: `CLAUDE.md`
- `cursor`: `.cursor/rules/learning-project-tutor.mdc`
- `generic`: `PROJECT_INSTRUCTIONS.md`

## Install

Install the skill into Codex:

```bash
mkdir -p ~/.codex/skills/learning-project-tutor
cp -R skill/* ~/.codex/skills/learning-project-tutor/
```

Create a learning workspace:

```bash
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform codex
```

Use `--platform claude-code`, `--platform cursor`, or `--platform generic` for other rule-file formats.

## Common Tasks

Create a workspace from this repo:

```bash
python3 skill/scripts/scaffold_learning_workspace.py /path/to/workspace --topic my-topic --platform codex
```

Add a topic to an existing workspace:

```bash
python3 starter-workspace/tools/create_topic_from_template.py /path/to/workspace causal-inference-basics
```

Build release archives:

```bash
bash scripts/release.sh dist
```

Release artifacts:
- `learning-project-tutor-<version>.zip`
- `learning-project-starter-workspace-<version>.zip`

## Demo

Open the demo source:
- `starter-workspace/topics/demo-proxy-metrics/00-source.md`
- `starter-workspace/topics/demo-proxy-metrics/README.md`

Then ask your agent:

```text
run learning cycle for topic demo-proxy-metrics
```
