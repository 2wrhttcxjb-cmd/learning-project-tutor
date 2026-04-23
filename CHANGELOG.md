# Changelog

## 0.2.2 - 2026-04-23
- quoted `skill/SKILL.md` description frontmatter so YAML parsers accept descriptions containing colons

## 0.2.1 - 2026-04-23
- revised public documentation to describe the current package structure and workspace model
- aligned skill, starter workspace, scaffolded README, demo README, and adapter wording
- kept implementation and teaching behavior unchanged

## 0.2.0 - 2026-04-23
- added platform adapters for Codex, Claude Code, Cursor, and generic agents
- added `--platform` support to workspace scaffolding
- updated install docs for multi-platform workspace generation

## 0.1.1 - 2026-04-23
- added `agents/openai.yaml` for the packaged skill
- added `scaffold_learning_workspace.py` for workspace bootstrapping
- added `create_topic_from_template.py` for new topic creation inside an existing workspace
- added short distribution references for teaching contract and state machine
- added `demo-proxy-metrics` as a runnable starter topic
- added repo-level release structure and release script

## 0.1.0 - 2026-04-23
- packaged the reusable learning workflow as `learning-project-tutor`
- packaged the minimal starter workspace
- added zip packaging script for skill and starter workspace artifacts
