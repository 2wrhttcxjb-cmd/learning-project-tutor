# Learning Project Starter Workspace

这个目录是展开后的 starter workspace。

它不是 skill 本体，而是一份可以直接复制给别人使用的最小学习工程。更适合下面两种场景：

1. 你想让别人直接解压后开始填 source
2. 你想把一套默认目录和初始文件一起交付

## Included
- `AGENTS.md`
- `SOURCE_TYPE_COURSE_PLANNING.md`
- `ACADEMIC_ARTICLE_METHOD.md`
- `templates/learning/`
- `tools/`
- `memory/`
- `topics/example-topic/`
- `topics/demo-proxy-metrics/`

## Suggested usage
1. 复制整个目录到对方自己的 Obsidian vault 或工作目录
2. 把 `topics/example-topic/` 复制或重命名成真实 topic 名
3. 在 `00-source.md` 里放入学习材料
4. 让 Codex 执行当前 topic 的 learning cycle

如果想直接从已带的 demo source 起步，可以先看：
- `topics/demo-proxy-metrics/00-source.md`
- `topics/demo-proxy-metrics/README.md`

## Starter topic convention
推荐新 topic 用短横线命名，例如：
- `deep-learning-recsys`
- `market-maps-ai-agents`
- `roman-empire-collapse`

每个新 topic 至少保留这些文件：
- `00-source.md`
- `00-course-map.md`
- `topic_state.yaml`
- `memory/topic-memory.yaml`
- `memory/current-context.md`
- `memory/reconsolidation-history.md`

也可以直接运行：

`python3 tools/create_topic_from_template.py <workspace-path> <topic-name>`

例如：

`python3 tools/create_topic_from_template.py . causal-inference-basics`

## Common prompts
- `run learning cycle for topic <topic-name>`
- `check learning state for topic <topic-name>`
- `answer a QA question for topic <topic-name>`
