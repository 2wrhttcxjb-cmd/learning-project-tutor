# Learning Project Starter Workspace

This is a starter workspace for source-based 1:1 tutoring.

It stores source material, generated lessons, learner responses, diagnoses, optional bridge or reframe lessons, QA logs, memory files, and final transfer tasks inside topic folders.

## Contents

- `AGENTS.md`: Codex rule file
- `adapters/`: rule templates for other platforms
- `SOURCE_TYPE_COURSE_PLANNING.md`
- `ACADEMIC_ARTICLE_METHOD.md`
- `templates/learning/`
- `tools/`
- `memory/`
- `topics/example-topic/`
- `topics/demo-proxy-metrics/`

## Topic Structure

Each topic contains:
- `00-source.md`
- `00-course-map.md`
- `topic_state.yaml`
- `lessons/`
- `responses/`
- `diagnosis/`
- `final/`
- `memory/`

## Start A Topic

1. Copy or rename `topics/example-topic/`.
2. Put source material in `00-source.md`.
3. Ask your agent:

```text
run learning cycle for topic <topic-name>
```

When the agent asks for a response, write your answer in the indicated response file before continuing.

## Other Platforms

This starter workspace defaults to Codex through `AGENTS.md`.

To generate another platform's rule file from the installed skill:

```bash
python3 scripts/scaffold_learning_workspace.py <workspace-path> --topic <topic-name> --platform claude-code
```

Adapters:
- `codex`: `AGENTS.md`
- `claude-code`: `CLAUDE.md`
- `cursor`: `.cursor/rules/learning-project-tutor.mdc`
- `generic`: `PROJECT_INSTRUCTIONS.md`

## Try The Demo

Open:
- `topics/demo-proxy-metrics/00-source.md`
- `topics/demo-proxy-metrics/README.md`

Then ask:

```text
run learning cycle for topic demo-proxy-metrics
```

## Add Topics Later

```bash
python3 tools/create_topic_from_template.py <workspace-path> <topic-name>
```

Example:

```bash
python3 tools/create_topic_from_template.py . causal-inference-basics
```
