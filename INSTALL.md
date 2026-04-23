# Install

## Codex Skill

Install the skill:

```bash
mkdir -p ~/.codex/skills/learning-project-tutor
cp -R skill/* ~/.codex/skills/learning-project-tutor/
```

Create a workspace for real learning:

```bash
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform codex
```

## Other Agent Platforms

Use the same scaffold command with a different adapter:

```bash
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform claude-code
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform cursor
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform generic
```

Generated rule files:
- `codex` -> `AGENTS.md`
- `claude-code` -> `CLAUDE.md`
- `cursor` -> `.cursor/rules/learning-project-tutor.mdc`
- `generic` -> `PROJECT_INSTRUCTIONS.md`

## Start From The Starter Workspace

If you want a ready-to-copy workspace instead of installing the skill first:

```bash
cp -R starter-workspace ~/learning-project
```

Then put source material in:

```text
~/learning-project/topics/example-topic/00-source.md
```

## Add Topics Later

```bash
python3 ~/learning-project/tools/create_topic_from_template.py ~/learning-project my-next-topic
```
