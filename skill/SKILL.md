---
name: learning-project-tutor
description: Use when the user wants to turn source material into a state-driven learning project with lessons, response files, diagnoses, bridge or reframe lessons, and final synthesis or transfer tasks. Good for Obsidian-based study workflows, source-driven self-learning, and reusable teaching loops that diagnose understanding before advancing.
---

# Learning Project Tutor

## Purpose
Run a reusable learning workflow that teaches from source material in small lessons, waits for a formal user response, diagnoses understanding, and only then decides whether to advance, bridge, or reframe.

This skill is the distributable entrypoint for the learning project. It should be installed as one skill folder and used to create or maintain a workspace that follows the same state-driven structure.

## Use This Skill When
- the user wants to learn from an article, paper, talk transcript, report, or book chapter
- the user wants lesson -> response -> diagnosis instead of one-shot summaries
- the user wants the next lesson to depend on demonstrated understanding
- the user wants a reusable learning workspace they can keep running across topics

## Core Teaching Contract
1. Always read the current topic state first.
2. Use `topic_state.yaml` as the control signal.
3. Perform exactly one formal state transition per learning-cycle run unless the user explicitly asks for more.
4. Never skip the formal response step.
5. Never generate the next lesson before a diagnosis is completed.
6. Keep each lesson focused on one small cognitive unit.
7. Questions must diagnose understanding, not just recall.
8. Diagnosis is a teaching decision, not a summary.

## Workspace Shape
When the user asks to set up a new learning workspace, create or maintain this structure:

- `AGENTS.md`
- `SOURCE_TYPE_COURSE_PLANNING.md`
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

For a concrete layout and file intent, read [references/workspace-layout.md](references/workspace-layout.md).

## Default Learning Cycle
For a topic that already has source material:

1. Read `AGENTS.md`.
2. Read `topics/<topic>/topic_state.yaml`.
3. Validate that the files required by the current status exist.
4. Do the one next action allowed by that status.
5. Update `topic_state.yaml`.

## Expected Status Flow
- `drafting_map`
- `ready_for_lesson`
- `waiting_user_response`
- `ready_for_diagnosis`
- `ready_for_next_action`
- `final_synthesis_ready`
- `final_transfer_ready`
- `waiting_transfer_response`
- `ready_for_transfer_diagnosis`
- `final_articulation_ready`
- `waiting_articulation_response`
- `ready_for_closure`
- `closed`

## Lesson Rules
- Explain why first, then what.
- Keep terminology lightweight and local to the lesson.
- Add a minimal term note when technical vocabulary is necessary.
- Do not pack multiple parallel mini-topics into one lesson.
- End every lesson with diagnostic questions sized to the lesson's true complexity.

## Diagnosis Rules
Every diagnosis must judge:
- whether the user understood the core claim
- whether the user understood the key causal link
- whether the user showed at least minimal transfer ability
- what kind of misunderstanding is present
- whether the next move should be `advance`, `bridge`, or `reframe`

Formal response is the primary evidence. QA logs can help interpret the response but cannot replace it.

## Final Phase Rules
Do not treat topic completion as "lesson path finished". A topic is only done after:
- synthesis
- transfer
- articulation
- closure

If transfer fails, reopen the loop with a bridge lesson instead of closing the topic.

## Packaging Guidance
When adapting this skill for another user or vault:
- keep the skill folder self-contained
- avoid hardcoding your personal vault paths
- keep reusable logic in this skill, not in topic output files
- ship templates and scripts only if they are broadly reusable
- do not ship your private topics, responses, or memory history unless the user explicitly wants examples

## Bundled Assets
- reusable templates live in `templates/learning/`
- reusable helper scripts live in `scripts/`
- stable workflow references live in `references/`
- UI metadata lives in `agents/openai.yaml`

Read these short references first:
- `references/teaching-contract.md`
- `references/state-machine.md`

Only read the full generated-workspace `AGENTS.md` when you need the complete lesson-writing and diagnosis constraints.

If the user wants a fresh workspace, run:

```bash
python3 scripts/scaffold_learning_workspace.py /target/workspace/path --topic my-first-topic
```

That scaffold creates the root learning workspace, memory baselines, one example topic, and copies the reusable templates and helper scripts into the target directory.

If the user already has a workspace and wants another topic skeleton, run:

```bash
python3 scripts/create_topic_from_template.py /existing/workspace my-next-topic
```

To copy from the packaged demo topic shape instead:

```bash
python3 scripts/create_topic_from_template.py /existing/workspace my-next-topic --from-demo
```

If the user wants release archives for sharing, run:

```bash
bash scripts/package_learning_project.sh /target/output-dir 0.1.0
```

This creates one zip for the skill and one zip for the starter workspace.

## Recommended Distribution Boundary
Package these as reusable assets:
- workflow rules
- state machine rules
- lesson and diagnosis design rules
- template files
- helper scripts that validate QA, build quote indexes, or preflight state

Do not package these as defaults:
- your existing topic data
- personal memory graph history
- user-specific notes
- one-off debugging artifacts
