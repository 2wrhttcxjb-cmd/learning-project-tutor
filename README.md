# Learning Project Tutor

一个可分发的学习工作流仓库，包含两部分：

- `skill/`: 可安装到 Codex skills 目录的 `learning-project-tutor` skill
- `starter-workspace/`: 可直接复制给别人的最小学习工程模板

## What this repo is for
- 把 source 驱动的 lesson -> response -> diagnosis 工作流打包成可复用 skill
- 给新用户一份开箱即用的 starter workspace
- 支持后续做 zip release 或单独拆成两个交付包

## Repo layout
- `skill/`
  Codex skill 本体，包含 `SKILL.md`、`agents/openai.yaml`、脚本、模板和参考规则
- `starter-workspace/`
  展开后的工作区模板，包含 `AGENTS.md`、`templates/learning/`、`tools/`、`memory/` 和 demo topics
- `scripts/release.sh`
  仓库级发布脚本，会同时打出 skill zip 和 starter workspace zip
- `VERSION`
  当前发布版本
- `CHANGELOG.md`
  版本变更记录

## Install

### Option 1: install the skill
把 `skill/` 目录复制到：

```bash
~/.codex/skills/learning-project-tutor/
```

然后初始化一个工作区：

```bash
python3 ~/.codex/skills/learning-project-tutor/scripts/scaffold_learning_workspace.py ~/learning-project --topic my-first-topic
```

### Option 2: copy the starter workspace
直接复制 `starter-workspace/` 到目标目录，然后开始填 `topics/<topic>/00-source.md`。

## Common commands

### Create a fresh workspace from the skill
```bash
python3 skill/scripts/scaffold_learning_workspace.py /path/to/workspace --topic my-topic
```

### Add a new topic inside an existing workspace
```bash
python3 starter-workspace/tools/create_topic_from_template.py /path/to/workspace causal-inference-basics
```

### Build release archives
```bash
bash scripts/release.sh dist
```

## Release artifacts
发布脚本默认产出两份 zip：
- `learning-project-tutor-<version>.zip`
- `learning-project-starter-workspace-<version>.zip`

## License
MIT. See `LICENSE`.

## Suggested first-run demo
如果想快速看这套 workflow 怎么工作，先打开：

- `starter-workspace/topics/demo-proxy-metrics/00-source.md`
- `starter-workspace/topics/demo-proxy-metrics/README.md`

然后运行：

```text
run learning cycle for topic demo-proxy-metrics
```
