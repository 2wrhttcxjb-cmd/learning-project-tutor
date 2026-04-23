## 目标
这是一个用 Obsidian + Codex 运行的个性化学习工程。

## 系统角色
- Obsidian：知识库、回答区、过程记录
- Codex：出题、诊断、生成下一课
- AGENTS.md：教学规则与流程控制

## 双层结构
- 执行层：每个 topic 自己的 `topic_state.yaml`，负责推进 lesson / response / diagnosis / final
- 记忆层：repo 根目录下的 `memory/`，负责跨 topic activation / schema compression / reconsolidation

默认情况下，记忆层不会改变主状态机，也不会替代 topic 内 lesson 流程；它只会在 diagnosis 之后、下一课之前影响“下一步该怎么教”。

## 学习闭环
1. 准备 source
2. 生成 lesson
3. 回答问题
4. 生成 diagnosis
5. 判断是否进入下一课，或插入 bridge lesson
6. 进入 final synthesis / transfer / articulation / closure

## 原则
- 不允许跳过 response 直接进入下一课
- 不允许没有 diagnosis 就生成下一课
- 不以打分为目标，以诊断误解为目标
- topic 之间相互隔离，避免上下文污染
- 不以“文件是否存在”驱动流程，而以 `topic_state.yaml` 驱动流程

## 使用方式
每个 topic 都应有一个 `topic_state.yaml`。这是流程控制中心，Codex 每次都应先读状态，再决定下一步。

### 1. 让系统推进一步
当你想让 Codex 执行当前 topic 的下一步时，可以直接说：

`run learning cycle for topic <topic-name>`

如果你要手动检查当前 cycle 入口，也可以运行：

`ruby tools/run_learning_cycle.rb <topic-name>`

系统会只做一件当前状态允许的事，例如：
- 生成下一节 lesson
- 检查 response 是否已经填写
- 生成 diagnosis
- 进入 final synthesis / transfer / articulation / closure

### 2. 用户需要做什么
当状态是下面这些时，Codex 不应自动跳过，必须等待你填写回答文件：
- `waiting_user_response`
- `waiting_transfer_response`
- `waiting_articulation_response`

你需要先去对应的 response 文件里作答，然后再让系统继续执行下一步。

### 3. 写完回答后怎么继续
写完后，再次对 Codex 说：

`run learning cycle for topic <topic-name>`

系统会检查预期 response 文件是否存在且非空：
- 如果已完成，就推进到下一状态
- 如果未完成，就指出还缺哪个文件
- 进入 `ready_for_next_action` 或 `ready_for_closure` 时，也会先执行 memory writeback，再继续后续动作

### 3.5. lesson 期间的即时问答旁路
在 `lesson -> response` 之间，你可以随时发起即时问答，不会打断主流程。

例如你可以说：
- `answer a QA question for topic <topic-name>`
- 或者直接问：
- `解释一下 lesson 里的 X`
- `Figure 2 在说什么`
- `这句原文是什么意思`

这些问答会进入旁路 QA：
- 可以帮助你理解当前 lesson
- 第一个旁路问题会初始化 `topics/<topic>/qa/QA_LOG.md`
- 初始化后，本 topic 后续 QA 会继续记入同一个 QA 文档，并按当前 lesson / final task 分 section
- 当前 `topic_state.yaml` 也会同步记录最小 QA 锚点，避免 QA 在 lesson 重写时丢失
- 但不会替代正式 `response`
- 也不会直接触发 `diagnosis`
- 在生成 diagnosis 时，当前 lesson 的 QA 会作为辅助证据读取
- 如果 QA 暴露出当前正式问题没有覆盖到的核心缺口，系统可以在 `response` 文件中追加一个 `QA Follow-up` 小区块

### 3.6. quote 画线与复习索引
如果你在阅读 lesson 时，遇到想保留的原文 quote、figure 说明或关键解释，可以像 Kindle 画线一样做轻量标记。

做法是在目标段落下面单独加一行：

```md
%%fav: %%
```

如果想顺手写备注，可以写成：

```md
%%fav: 这句适合复习 example age 的作用%%
```

之后可以让 Codex 或直接运行：

`python3 tools/build_quote_index.py <topic-name>`

系统会生成：
- `topics/<topic-name>/quotes/QUOTE_INDEX.md`

这个文件会汇总：
- 你标记过的 quote / figure /解释段落
- 它们所在的 lesson / QA 跳转位置
- 如果有 `Source:`，也会带上原文定位说明

如果当前 lesson 的 `response` 已经写完，那么你下一次触发 learning cycle 时，系统也会先自动刷新一次这个索引，再继续 diagnosis 或后续步骤。

如果你不想手动跑脚本，平时直接继续 learning cycle 就够了；手动运行更适合你想立即单独刷新索引的时候。

### 4. 状态不一致时怎么检查
如果你怀疑状态和文件不同步，可以说：

`check learning state for topic <topic-name>`

系统会报告：
- 缺失文件
- 空文件
- 状态与文件引用不一致
- 建议修复方式

### 5. 一条最小工作流
1. 你说：`run learning cycle for topic <topic-name>`
2. Codex 生成 lesson 或 diagnosis，或者提示等待你作答
3. 如果中途有疑问，可以先走 QA 旁路提问，但主状态不变
4. 你填写对应 response 文件
5. 你再说：`run learning cycle for topic <topic-name>`
