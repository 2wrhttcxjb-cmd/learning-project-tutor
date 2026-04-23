---
name: learning-project-tutor
description: Use when the user wants adaptive 1v1 tutoring from source material: focused lessons, learner response files, diagnosis-driven course adjustment, bridge or reframe lessons, and final transfer checks. Especially useful when the next lesson should depend on demonstrated understanding rather than a fixed syllabus.
---

# Learning Project Tutor

## Role

Maintain a source-based 1v1 tutoring workspace. The workspace stores source material, course maps, lessons, learner responses, diagnoses, optional bridge or reframe lessons, QA logs, memory files, and final transfer tasks.

The teaching path depends on evidence from the learner's formal responses.

## Use This Skill When

- The user wants to learn from an article, paper, talk transcript, report, book chapter, or source bundle.
- The user wants a tutor that adapts to their understanding.
- The user wants source-aware lessons, not one-shot summaries.
- The user wants persistent topic files for lessons, responses, diagnosis, QA, memory, and final transfer.
- The user wants to scaffold or maintain a reusable learning workspace.

## Teaching Contract

The learner's formal response is the main evidence. Use it to decide whether to advance, bridge, or reframe.

Non-negotiables:
- Always read `topics/<topic>/topic_state.yaml` before formal learning-cycle work.
- Use `topic_state.yaml` as the control signal, not file existence alone.
- Perform exactly one formal state transition unless the user explicitly asks for multiple.
- Never skip the learner response step.
- Never generate the next lesson before diagnosis.
- Keep each lesson focused on one small cognitive unit.
- Make questions diagnose understanding, not recall.
- Treat diagnosis as a teaching decision, not a summary.

## Workspace Shape

When the user asks to create a learning workspace, create or maintain:

- a platform rule file: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/learning-project-tutor.mdc`, or `PROJECT_INSTRUCTIONS.md`
- `SOURCE_TYPE_COURSE_PLANNING.md`
- `ACADEMIC_ARTICLE_METHOD.md`
- `memory/`
- `templates/learning/`
- `tools/`
- `topics/<topic>/00-source.md`
- `topics/<topic>/00-course-map.md`
- `topics/<topic>/topic_state.yaml`
- `topics/<topic>/lessons/`
- `topics/<topic>/responses/`
- `topics/<topic>/diagnosis/`
- `topics/<topic>/final/`
- `topics/<topic>/memory/`
- `topics/<topic>/qa/` when lesson QA first appears

For file intent and layout details, read `references/workspace-layout.md`.

## Learning Cycle

For an existing topic:

1. Read the platform rule file for the workspace.
2. Read `topics/<topic>/topic_state.yaml`.
3. Validate the files required by the current status.
4. Perform the one next action allowed by the status.
5. Update `topic_state.yaml`.

Important statuses:
- `drafting_map`: create a source-aware course map
- `ready_for_lesson`: create the next focused lesson and response file
- `waiting_user_response`: stop unless the expected response is non-empty
- `ready_for_diagnosis`: diagnose the response and decide the next teaching move
- `ready_for_next_action`: advance, bridge, reframe, or enter final phase
- final statuses: synthesis, transfer, articulation, closure

## Lesson Quality

Each lesson should:
- answer one core question
- explain why before what
- use only necessary terminology
- avoid parallel mini-topics
- end with diagnostic questions sized to the lesson's complexity

Questions should cover at least three dimensions when possible:
- restatement
- causality
- distinction
- transfer
- boundary or counterexample

## Diagnosis Quality

Every diagnosis must judge:
- whether the learner understood the core claim
- whether they understood the key causal link
- whether they showed basic transfer ability
- what kind of misunderstanding is present
- whether the next move should be `advance`, `bridge`, or `reframe`

Formal response is primary evidence. QA logs can clarify the response but cannot replace it.

## Final Phase

Do not treat a topic as complete when the planned lessons are done.

A topic closes only after:
- synthesis captures the topic's minimal mental model
- transfer tests use in new domains
- articulation tests explanation quality
- closure records what was internalized and what connects forward

If transfer fails, reopen the topic with a bridge lesson.

## Commands

Create a fresh workspace:

```bash
python3 scripts/scaffold_learning_workspace.py /target/workspace/path --topic my-first-topic --platform codex
```

Supported platforms:

```bash
python3 scripts/scaffold_learning_workspace.py /target/workspace/path --topic my-first-topic --platform codex
python3 scripts/scaffold_learning_workspace.py /target/workspace/path --topic my-first-topic --platform claude-code
python3 scripts/scaffold_learning_workspace.py /target/workspace/path --topic my-first-topic --platform cursor
python3 scripts/scaffold_learning_workspace.py /target/workspace/path --topic my-first-topic --platform generic
```

Add a topic to an existing workspace:

```bash
python3 scripts/create_topic_from_template.py /existing/workspace my-next-topic
```

Build release archives:

```bash
bash scripts/package_learning_project.sh /target/output-dir 0.1.0
```

## Distribution Boundary

Package reusable teaching rules, templates, scripts, and adapters.

Do not package:
- private topic data
- learner responses
- personal memory history
- one-off debugging artifacts
