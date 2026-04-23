# Source-Type Course Planning

## Purpose
这份文档提供一套可执行的课程规划规则，用来支持不同类型的 source，而不是默认把所有材料都按论文或按 section 数量来拆课。

目标不是让所有 source 用同一种写法，而是让不同 source type 最终都能收敛成稳定的 `00-course-map.md` 结构和合理的 lesson budget。

## Shared workflow
无论 source type 是什么，规划时都先做这 5 步：

1. 识别 dominant source type
2. 在 `00-course-map.md` 写出 `Source Profile`
3. 写 `Source Structure`
4. 写 `Coverage Plan`
5. 再把 coverage unit 聚合成正式 `Course Map`

## Required `Source Profile`
每个 `00-course-map.md` 都应包含一个 `Source Profile`，至少回答：

- dominant source type
- source scope
- approximate length or structural granularity
- formal density
- evidence mode
- recommended lesson budget
- budget rationale

`budget rationale` 不是装饰；它的作用是强迫规划者说明：
- 为什么这份 source 值得这么多 lesson
- 为什么这些 lesson 各自值得经历一次独立的 `lesson -> response -> diagnosis`

## Normalized planning interface
无论 source type 是什么，`00-course-map.md` 都尽量保持下面的结构：

1. `Source Profile`
2. `Source Structure`
3. `Goal`
4. `Source`
5. `Coverage Plan`
6. `Course Map`
7. `Notes`

这样 orchestrator 和后续 lesson generation 可以使用统一入口，而不会因为 source type 改变就失去稳定格式。

## Source types and default planning patterns

### `paper`
适用：
- 学术论文
- 有明确 problem / method / evidence / conclusion 结构的研究报告

主线优先级：
- claim / abstract
- background
- hypothesis or framing
- method
- evidence
- conclusion

lesson budget 经验值：
- 高形式化单篇 paper：通常 `5-8`
- 如果变量、公式、实验链条很多，可以更多

### `engineering_case_blog`
适用：
- 工程案例复盘
- 方法论博客
- 单篇产品/agent/harness 设计文章

主线优先级：
- author claim
- failure mode or problem pressure
- design pattern / architecture
- case evidence
- simplification or transfer principle

lesson budget 经验值：
- 单篇 `3k-7k` 文章：通常 `4-6`

特别规则：
- 不要把每个 agent persona 单独拆成一课，除非它真的形成独立因果链
- 不要把 opening、case study、结尾感想都各拆成一课
- 如果两个案例共同支撑一个判断，优先聚合成同一课

### `market_report`
适用：
- market map
- 行业概览
- 投资 thesis
- 结构化行业报告

主线优先级：
- thesis
- segmentation / framework
- trend evidence
- strategic implication

lesson budget 经验值：
- 单篇或单份中等报告：通常 `3-5`

特别规则：
- 不要默认把每个 layer / subsector / company list 都拆成 lesson
- 先教“作者用什么框架看市场”，再决定哪些证据值得单独拉出

### `evergreen_nonfiction`
适用：
- 普通商业文章
- popular science
- 概念驱动的非虚构解释文

主线优先级：
- core claim
- distinctions
- mechanism
- example
- boundary

lesson budget 经验值：
- 单篇文章或单章：通常 `3-5`

特别规则：
- 例子默认服务主命题，不默认单独成课
- 先把 causal chain 讲清，再补术语

### `essay_series`
适用：
- 主题相关文章集
- blog series
- 多篇访谈或 essay 围绕同一主题

主线优先级：
- theme cluster
- cross-document agreement
- meaningful disagreement
- synthesis

lesson budget 经验值：
- 取决于文档数与主题簇数量；通常按 theme cluster 定 lesson，不按文档数

特别规则：
- 不按发布时间排序
- 不把每课做成多文档摘要堆叠

### `book`
适用：
- 长书
- 章节化长文本

主线优先级：
- bounded packet
- local author move
- prerequisite link
- next packet planning

lesson budget 经验值：
- 不预先用整本书总页数决定
- 先做 slice / packet，再按 packet 规划

特别规则：
- 每课只读有限 packet
- 不要求每课重新扫描整本书

### `talk_or_interview`
适用：
- 演讲稿
- podcast transcript
- 访谈

主线优先级：
- thesis
- reasoning turn
- story or example
- caveat

lesson budget 经验值：
- 单篇 transcript：通常 `2-4`

特别规则：
- 不按时间轴机械切段
- 按 speaker 的论证转折点聚合

### `mixed`
适用：
- 多种材料混合

默认规则：
- 先选一个 dominant source type
- 其余 source 先作为辅助材料，而不是立即让课程规划混合失控

## Lesson budget heuristics
lesson 数量不是按字数线性增长，而是按“独立论证动作的数量”决定。

经验规则：
- 非常短、单主张材料：`1-2`
- `1.5k-4k` 的低到中等形式化单篇文章：`2-4`
- `4k-7k` 的工程案例、方法文或中等报告：`4-6`
- 高形式化论文、密集章节或多套机制并存材料：`5+`

一个内容点只有同时满足下面条件，才值得单独成为正式 lesson：
- 有独立核心问题
- 有完整因果链或证据链
- 能支撑 `2-5` 个不重复的诊断问题
- 不单独诊断就难以安全进入下一步

## Aggregation checklist
从 coverage plan 聚合到 course map 前，先检查：

- coverage unit 数和 lesson 数是不是几乎一样
- lesson 是否只是照 section 标题切开
- 开头和结尾是否只是重复同一主张，却被拆成两课
- 一个例子是否被从它支撑的主命题里硬拆出来
- lesson 是否值得一次独立 response / diagnosis

如果以上任一项答案偏向 yes，通常说明 lesson 被切得太碎。

## Common red flags
- “coverage plan 不等于 lesson map” 写在文档里，但实际还是一对一映射
- 每个 section heading 都变成一课
- 每个 framework layer 或 company bucket 都变成一课
- 为了凑 lesson 数，把本应在 final synthesis 中回收的 meta 结论额外拆成一课
- 课后问题太少，只能围绕同一句话换说法

## Recommended planning check
正式落 `Course Map` 前，至少回答这两个问题：

1. 这份 source 的 lesson budget 是否和 source type 相匹配？
2. 如果用户真的要经历这么多次 `response -> diagnosis`，每一回合都值得吗？

如果回答不够坚定，优先压缩 lesson 数量，再依赖 bridge lesson 处理真实暴露出的理解缺口。
