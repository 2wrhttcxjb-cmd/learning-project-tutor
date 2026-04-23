# Academic Article Method

## Purpose
当 source 的主要材料是学术论文时，课程设计不应先按术语或模块列表拆解，而应优先对齐论文原文的论证链条。

## Core idea
把论文看成一个有明确推进顺序的论证过程，而不是一个知识点仓库。

lesson 的顺序优先对应这些环节：
- 主张 / 摘要
- 问题背景
- 假设
- 方法
- 实验 / 证据
- 结论

但不能把“原文覆盖单元”和“最终课程单元”混成一层。

## Two-layer design
学术论文课程应至少分成两层，但它们可以收纳在同一个 `00-course-map.md` 中：

1. `coverage plan`
- 用最小论证动作拆原文
- 目标是防止遗漏变量、公式、机制、比较和工程取舍
- 它不是最终 lesson map

2. `lesson map`
- 把多个相邻、同向的 coverage unit 聚合成一节课
- 目标是保证容量合理、逻辑完整、提问有抓手

## Aggregation rule
聚合时优先按“同一个论证任务”合并，而不是按段落数量平均切。

适合合并到同一课的内容：
- 同一个核心问题下的定义 + 变量 + 公式
- 同一个机制的解释 + 为什么这样设计
- 同一类工程取舍的多步展开

不适合合并到同一课的内容：
- 问题重定义和实验结论
- 方法定义和结果比较
- candidate generation 和 ranking
- 一个 lesson 内需要跨越太多新的变量系统

## Lesson size rule
学术论文 lesson 不应过小。

如果一节课只讲一个非常窄的小概念，通常会带来两个问题：
- 课后问题变得模糊、低质量，只能围绕同一句话打转
- 用户还没形成一个完整逻辑块，就被迫作答

更合理的 lesson 容量通常应满足：
- 能覆盖一个完整的论证动作
- 能提出与 lesson 容量匹配的 2-5 个有区分度的问题
- 问题能够明确对应原文中的对象、关系或判断

## Lesson coherence rule
学术论文 lesson 也不能只是把同一小节里出现过的内容平铺罗列。

更稳的写法是，先把本课压成一个单句主问题，再让全课只回答这一个问题。

建议在正式写 lesson 之前，先写出 1 句 thread：
- 因为作者要解决什么问题
- 所以先引入什么对象或约束
- 再用什么机制 / figure / table 把它落地
- 最后得到什么判断

正文里的每个大段都应当能明确对应这条 thread 的一个位置：
- setup
- mechanism
- evidence
- implication

如果某一段无法解释它在这条主线里承担什么作用，通常有三种处理：
- 删掉
- 挪到下一课
- 改写成服务当前主线的补充说明

避免的典型坏形态：
- 同一课里并列堆 4-5 个互相平行的小主题
- 前一段还在讲“对象是什么”，后一段突然跳去复述全文结论
- figure、table、conclusion 都出现了，但彼此没有被串成一个因果链

## Question quality rule for academic lessons
学术论文课后的问题，不应只围绕单一句子反复换说法。

问题优先覆盖：
- 作者在这一节到底做了什么动作
- 原文中的变量 / 公式 / 机制在表达什么
- 作者为什么要这样定义或这样取舍
- 这一节与前文或旧方法相比改变了什么

如果 lesson 中包含变量、公式或符号系统，问题不应考记忆性映射，例如“某个变量对应哪个字母”。
更好的问法通常是：
- 哪些变量或输入共同影响作者要预测的对象
- 这个关系式整体上在表达什么
- 为什么这些变量都属于同一个问题定义的一部分

避免：
- 太泛的问题
- 看不出在问什么对象的问题
- 只要求换句话说但没有新认知动作的问题

## Problems seen in the last round
以 `YouTube-RCMD` 的 `Lesson 05` 为例，上一轮提问暴露出几类典型问题：

- 问题把不同层级的对象并列，例如把表示机制和训练信号放进同一个问句
- 语义边界不清，用户难以判断题目究竟在问“概念作用”还是“工程取舍”
- 有些问题太贴近符号或字面层，容易滑向低价值记忆
- 某些问题虽然表面不同，但实际上都在追问同一件事，区分度不够

这些问题会导致两种后果：
- 用户被题目本身误导，而不是被原文难点难住
- response 看似简短，其实是在替题目补语义，而不是在暴露真实理解

## Optimized question scheme
更稳的学术课提问方案，建议按下面顺序生成：

1. `Core move`
- 问作者这一节到底做了什么动作
- 例如：重定义了问题、引入了新变量系统、解释了某个机制、做了某个取舍

2. `Structure of the move`
- 问这个动作是由哪些对象、变量、机制搭起来的
- 强调“哪些因素共同作用”，而不是“某个符号对应什么字母”

3. `Why this move`
- 问作者为什么要这样定义或这样取舍
- 可与旧方法、直觉说法、上一节主线做对比

4. `Optional transfer or boundary`
- 只有当 lesson 容量足够且这一节确实形成了一个完整逻辑块时，才加入迁移或边界题

## Question drafting checklist
正式落题前，先过一遍下面的检查：

- 这道题问的对象是否单一且清楚
- 题目是否把不同层级的概念硬并列了
- 用户是否能从题干里直接看出自己要解释什么
- 题目是否在考理解关系，而不是考记忆细节
- 这几道题之间是否各自承担不同诊断作用，而不是重复换说法

## Workflow
1. 先判断 source 是否是学术论文
2. 提取论文的行文结构与论证链条
3. 在 `00-course-map.md` 中先写 `Source Structure`
4. 再写 `Coverage Plan`
5. 最后写正式 `Course Map`
6. 每一节 lesson 对应一个完整的教学单元，而不是一个过小的原子概念
7. lesson 结尾生成与 lesson 容量匹配的 2-5 个诊断问题
8. 等待 response
9. 先做 diagnosis，再决定 advance / bridge / reframe

## Evidence rule
学术论文类 lesson 不能只凭空描述。

必须尽量引用：
- 原文关键句
- 原文中的 figure / diagram

引用不应集中堆在一个单独 section 里。
更稳的写法是：
- 在解释某个知识点、变量关系、机制、数据结论时，紧接着放支撑它的原文
- 让 figure / diagram 出现在它真正被讨论和解读的位置
- 让用户能直接看到“这句解释对应原文哪一部分”

对重要 figure / chart，解释不能停在“这张图证明了什么”。
至少还要补出：
- x 轴和 y 轴各自表示什么
- 指标或单位是什么意思
- 图例里的线、柱、颜色或分组分别代表什么
- 读图时最值得关注的是哪一段差异、趋势、拐点或对比

目标不是把图的每个细节都讲完，而是把“这张图该怎么看”讲清楚。

引用格式：

### Paper Quote
> [Paper Quote]
> 原文关键句
> Source: Abstract / Introduction / Section X

### Paper Figure
> [Paper Figure]
> Figure X: 原图标题或原图在论证中的作用
> Source: Figure X

如果本地已有图像文件，可以在 `Paper Figure` 后加入图片嵌入。

### Paper Table
> [Paper Table]
> Table X: 这张表在当前 lesson 中支撑的判断
> Source: Table X

如果本地已裁出表格图像，优先附上图片嵌入，并像 figure 一样纳入 manifest 校验。

### Paper Formula
> [Paper Formula]
> Formula X: 这条公式在当前 lesson 中支撑的判断
> Source: Formula X / Equation X

如果本地已裁出公式图像，优先附上图片嵌入，并要求公式编号或周边标签与 lesson 引用一致。

## Figure extraction workflow
为避免把错误页图当成目标 figure 插进 lesson，学术论文中的 figure 应按下面正向流程处理：

1. 先在 PDF 文本或 review 提取稿里定位 `Figure N` 的 caption
2. 再渲染包含该 caption 的准确 PDF 页，而不是直接猜现有 page image
3. 从该页裁出“图 + caption”，保存为 `source-extracts/page-images/figure-N.png`
4. 在 `source-extracts/figure-manifest.yaml` 中登记：
   - `figure_id`
   - source page render
   - extracted image path
   - caption verification source
   - verification status
5. 只有 manifest 中标记为 `verified` 的 figure，才允许被 lesson 正式嵌入

对 table / formula 也采用同样的流程，只是把 `figure_id` 换成 `table_id` 或 `formula_id`，并把 `Paper Figure` 换成对应的 `Paper Table` / `Paper Formula`。

推荐优先使用独立 skill：
- `skills/extract-paper-figures/SKILL.md`

## Figure validation rule
当 lesson 中使用本地图像时，必须同时满足：
- `Paper Figure` 块中的 `Source: Figure N` 与图片文件 `figure-N.png` 一致
- 图片路径在本地存在
- `figure-manifest.yaml` 中有对应 `Figure N` 的 verified 记录

推荐在更新论文 lesson 后运行：

```bash
python3 tools/verify_figure_references.py <topic-name>
```

这个校验至少应拦住三类错误：
- 用错误页图冒充目标 figure
- lesson 写了 `Figure N`，但本地没有对应图像
- lesson 的图片路径与 manifest 中已验证的 figure 不一致
- lesson 写了 `Table N`，但没有对应表格图像或 manifest 记录
- lesson 写了 `Formula N` / `Equation N`，但没有对应公式图像或 manifest 记录

## Padding rule
裁切图像时，默认保留四周等长的合理 padding，避免图片过紧、贴边或视觉上失衡。

建议：
- figure / table / formula 都统一使用同一种 padding 策略
- 如果资产四周空间不够，优先调整裁切框，而不是把 padding 压成不对称
- 只在页面边缘阻挡时才允许局部截断，但要尽量保留均衡留白

## Common failure modes
最近一轮 `YouTube-RCMD` 的 figure 插图失败，暴露出两类常见问题：

1. 把 page crop 当成 figure crop
- 一页上可能同时有多个 figure、caption 和正文
- 如果只是凭页面位置大致截一下，很容易把相邻 figure 或正文一起带进去

2. 图和 caption 没有被当成同一个证据块
- 只截图不截 caption，lesson 里就失去 figure 编号核对
- 只截 caption 或 caption + 正文，也会让 lesson 里的图失去可读性

更稳的裁切原则是：
- 一个 lesson 资产 = 一个 figure block
- 这个 block 至少包含完整图像和对应 caption
- 默认不要包含相邻正文；如果必须保留少量空白，宁可留白，不要带入下一段正文
- 这个 block 周围应保持四边近似等长的 padding

## What changed in this branch
- 在 `AGENTS.md` 中增加了学术论文专用规则
- 将论文前置分析收纳进 `00-course-map.md`
- 将 `YouTube-RCMD` 的 `course map` 改成对齐论文原文逻辑链条
- 将 `Lesson 01` 改成从论文摘要主张出发，并引用原文句子与 Figure 2

## Current limits
- figure 引用依赖本地图像文件能被 Markdown 查看环境正确加载
- PDF 自动抽取仍不稳定，课程设计目前仍以“人工审读后抽取主线”为主
- 图像在不同渲染环境中的路径规则可能不同，必要时需要改用该环境原生嵌入格式
