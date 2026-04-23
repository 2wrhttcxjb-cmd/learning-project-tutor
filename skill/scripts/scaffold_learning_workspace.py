#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


MEMORY_STATE = """---
graph_version: 1
status: active
last_rebuilt_at: null
last_reconsolidated_at: null
last_active_topic: null
last_writeback_summary: null
"""

NODES_YAML = """---
nodes: []
"""

EDGES_YAML = """---
edges: []
"""

SCHEMA_INDEX = """# Schema Index

当前还没有稳定 schema。
当多个 topic 开始出现可压缩的共同结构时，再把它们整理到这里。
"""

ACTIVATION_LOG = """# Activation Log

这个文件记录正式 learning cycle 中发生的跨 topic activation / reconsolidation。
新的 topic 在完成 diagnosis 或 closure 后，才会开始追加记录。
"""

TOPIC_STATE = """topic_title: {topic_title}
status: drafting_map
current_unit: null
current_lesson_file: null
current_response_file: null
current_diagnosis_file: null
pending_user_action: null
last_decision: null
qa_open: false
qa_affects_response: false
qa_followup_needed: false
qa_file: qa/QA_LOG.md
current_qa_scope: null
current_qa_entry_count: 0
qa_last_recorded_at: null
final_phase_started: false
final_transfer_passed: false
final_articulation_done: false
topic_closed: false
last_lesson_memory_writeback_key: null
last_topic_memory_writeback_key: null
last_activated_nodes: []
"""

TOPIC_SOURCE = """# Source

把你要学习的原始材料放在这里。

推荐内容：
- 原文链接或出处
- 摘录正文
- 如果是论文，可附 PDF 文件名或相关图表路径
- 如果是多材料主题，先说明哪一个是 dominant source
"""

TOPIC_MAP = """# Course Map

在 `drafting_map` 状态下，由 Codex 根据 source 生成。
"""

TOPIC_MEMORY = """core_claim: null
causal_chain: []
distinctions: []
misconceptions: []
retrieval_cues: []
node_refs:
  concepts: []
  schemas: []
  episodes: []
"""

CURRENT_CONTEXT = """# Current Memory Context

当前还没有激活的跨 topic 教学上下文。
"""

RECON_HISTORY = """# Reconsolidation History

当前 topic 还没有发生正式记忆回写。
"""

README = """# Learning Project Starter Workspace

这是由 `learning-project-tutor` skill 生成的最小学习工程。

## How to use
1. 把学习材料放到 `topics/<topic>/00-source.md`
2. 确认 `topics/<topic>/topic_state.yaml` 的状态
3. 让 Codex 运行当前 topic 的下一步

## Common prompts
- `run learning cycle for topic <topic-name>`
- `check learning state for topic <topic-name>`
- `explain lesson 里的某个句子或 figure`

## What is already included
- `AGENTS.md`
- `SOURCE_TYPE_COURSE_PLANNING.md`
- `ACADEMIC_ARTICLE_METHOD.md`
- `templates/learning/`
- `tools/`
- `memory/`
- 一个示例 topic 骨架
- 一个可直接试跑的 demo topic
"""

DEMO_README = """# Demo Topic

这个 demo topic 用来展示：
- `00-source.md` 可以怎么写
- 一个短 source 如何进入 `drafting_map`
- 第一次跑 learning cycle 时，Codex 会如何先生成 course map
"""

DEMO_SOURCE = """# Source

## Title
Proxy metrics vs real outcomes

## Type hint
evergreen nonfiction article

## Source text

很多团队在做产品优化时，会先选择一个容易测量的指标，例如点击率、打开率或停留时长。这样做并不一定错，因为这些指标让团队能更快看到变化，也更容易做实验。

问题在于，容易测量的指标不一定等于真正想要的结果。点击率提高，可能只是标题更诱导；停留时长增加，可能只是流程更绕，而不是用户真的更满意。

因此，一个成熟的判断方式不是拒绝代理指标，而是先问两个问题：第一，这个指标和真实目标之间的关系是什么；第二，当团队开始优化这个指标时，系统最可能被扭曲成什么样子。

如果这两个问题说不清楚，团队就容易把“更会优化指标”误认为“更接近真实价值”。代理指标仍然有用，但它应该被当成近似入口，而不是终点本身。
"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_tree_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a starter learning workspace from the learning-project-tutor skill."
    )
    parser.add_argument("target", help="Target workspace directory")
    parser.add_argument(
        "--topic",
        default="example-topic",
        help="Initial topic directory name to create inside topics/",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    target = Path(args.target).expanduser().resolve()
    topic = args.topic.strip()
    if not topic:
        raise SystemExit("topic must not be empty")

    target.mkdir(parents=True, exist_ok=True)
    write_text(target / "README.md", README)

    references = skill_root / "references"
    shutil.copy2(references / "AGENTS.md", target / "AGENTS.md")
    shutil.copy2(references / "SOURCE_TYPE_COURSE_PLANNING.md", target / "SOURCE_TYPE_COURSE_PLANNING.md")
    shutil.copy2(references / "ACADEMIC_ARTICLE_METHOD.md", target / "ACADEMIC_ARTICLE_METHOD.md")

    copy_tree_contents(skill_root / "templates" / "learning", target / "templates" / "learning")
    copy_tree_contents(skill_root / "scripts", target / "tools")

    write_text(target / "memory" / "memory_state.yaml", MEMORY_STATE)
    write_text(target / "memory" / "nodes.yaml", NODES_YAML)
    write_text(target / "memory" / "edges.yaml", EDGES_YAML)
    write_text(target / "memory" / "schema-index.md", SCHEMA_INDEX)
    write_text(target / "memory" / "activation-log.md", ACTIVATION_LOG)

    topic_dir = target / "topics" / topic
    (topic_dir / "lessons").mkdir(parents=True, exist_ok=True)
    (topic_dir / "responses").mkdir(parents=True, exist_ok=True)
    (topic_dir / "diagnosis").mkdir(parents=True, exist_ok=True)
    (topic_dir / "final").mkdir(parents=True, exist_ok=True)
    (topic_dir / "memory").mkdir(parents=True, exist_ok=True)

    write_text(topic_dir / "00-source.md", TOPIC_SOURCE)
    write_text(topic_dir / "00-course-map.md", TOPIC_MAP)
    write_text(topic_dir / "topic_state.yaml", TOPIC_STATE.format(topic_title=topic))
    write_text(topic_dir / "memory" / "topic-memory.yaml", TOPIC_MEMORY)
    write_text(topic_dir / "memory" / "current-context.md", CURRENT_CONTEXT)
    write_text(topic_dir / "memory" / "reconsolidation-history.md", RECON_HISTORY)

    demo_dir = target / "topics" / "demo-proxy-metrics"
    (demo_dir / "lessons").mkdir(parents=True, exist_ok=True)
    (demo_dir / "responses").mkdir(parents=True, exist_ok=True)
    (demo_dir / "diagnosis").mkdir(parents=True, exist_ok=True)
    (demo_dir / "final").mkdir(parents=True, exist_ok=True)
    (demo_dir / "memory").mkdir(parents=True, exist_ok=True)

    write_text(demo_dir / "README.md", DEMO_README)
    write_text(demo_dir / "00-source.md", DEMO_SOURCE)
    write_text(demo_dir / "00-course-map.md", TOPIC_MAP)
    write_text(demo_dir / "topic_state.yaml", TOPIC_STATE.format(topic_title="demo-proxy-metrics"))
    write_text(demo_dir / "memory" / "topic-memory.yaml", TOPIC_MEMORY)
    write_text(demo_dir / "memory" / "current-context.md", CURRENT_CONTEXT)
    write_text(demo_dir / "memory" / "reconsolidation-history.md", RECON_HISTORY)

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
