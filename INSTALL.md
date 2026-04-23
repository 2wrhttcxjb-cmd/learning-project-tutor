# Install Commands

## Install the skill into Codex

```bash
mkdir -p ~/.codex/skills
cp -R skill ~/.codex/skills/learning-project-tutor
```

如果你希望目标目录名就是 skill 名，也可以用：

```bash
mkdir -p ~/.codex/skills/learning-project-tutor
cp -R skill/* ~/.codex/skills/learning-project-tutor/
```

## Create a new workspace

```bash
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform codex
```

## Platform adapters

The scaffold script can generate platform-specific instruction files:

```bash
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform codex
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform claude-code
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform cursor
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic --platform generic
```

Generated rule files:
- `codex` -> `AGENTS.md`
- `claude-code` -> `CLAUDE.md`
- `cursor` -> `.cursor/rules/learning-project-tutor.mdc`
- `generic` -> `PROJECT_INSTRUCTIONS.md`

## Start from the demo workspace directly

```bash
cp -R starter-workspace ~/learning-project
```

## Add a new topic later

```bash
python3 ~/learning-project/tools/create_topic_from_template.py ~/learning-project my-next-topic
```
