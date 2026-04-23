#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


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

建议至少包含：
- 材料标题
- 原文链接或出处
- 主要正文或摘录
- 如果是 mixed source，标出 dominant source
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

TEMPLATE_README = """# Topic Template

## How to start
1. 把 source 材料写进 `00-source.md`
2. 保持 `topic_state.yaml` 为 `drafting_map`
3. 让 Codex 执行：
   `run learning cycle for topic {topic_name}`

## Naming
推荐 topic 用短横线命名，例如：
- `proxy-metrics-vs-real-outcomes`
- `deep-learning-recsys`
- `roman-empire-collapse`
"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new topic skeleton inside an existing learning workspace."
    )
    parser.add_argument("workspace", help="Existing learning workspace root")
    parser.add_argument("topic", help="New topic name, for example proxy-metrics-vs-real-outcomes")
    parser.add_argument(
        "--from-demo",
        action="store_true",
        help="Copy the demo topic shape from topics/demo-proxy-metrics if it exists",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    topic_name = args.topic.strip()
    if not workspace.exists():
        raise SystemExit(f"workspace not found: {workspace}")
    if not topic_name:
        raise SystemExit("topic must not be empty")

    topics_dir = workspace / "topics"
    topic_dir = topics_dir / topic_name
    if topic_dir.exists():
        raise SystemExit(f"topic already exists: {topic_dir}")

    demo_dir = topics_dir / "demo-proxy-metrics"
    if args.from_demo and demo_dir.exists():
        shutil.copytree(demo_dir, topic_dir)
        state_path = topic_dir / "topic_state.yaml"
        state_text = state_path.read_text(encoding="utf-8").replace("demo-proxy-metrics", topic_name)
        state_path.write_text(state_text, encoding="utf-8")
        readme_path = topic_dir / "README.md"
        if readme_path.exists():
            readme_text = readme_path.read_text(encoding="utf-8").replace("demo-proxy-metrics", topic_name)
            readme_path.write_text(readme_text, encoding="utf-8")
        print(topic_dir)
        return 0

    (topic_dir / "lessons").mkdir(parents=True, exist_ok=True)
    (topic_dir / "responses").mkdir(parents=True, exist_ok=True)
    (topic_dir / "diagnosis").mkdir(parents=True, exist_ok=True)
    (topic_dir / "final").mkdir(parents=True, exist_ok=True)
    (topic_dir / "memory").mkdir(parents=True, exist_ok=True)

    write_text(topic_dir / "README.md", TEMPLATE_README.format(topic_name=topic_name))
    write_text(topic_dir / "00-source.md", TOPIC_SOURCE)
    write_text(topic_dir / "00-course-map.md", TOPIC_MAP)
    write_text(topic_dir / "topic_state.yaml", TOPIC_STATE.format(topic_title=topic_name))
    write_text(topic_dir / "memory" / "topic-memory.yaml", TOPIC_MEMORY)
    write_text(topic_dir / "memory" / "current-context.md", CURRENT_CONTEXT)
    write_text(topic_dir / "memory" / "reconsolidation-history.md", RECON_HISTORY)

    print(topic_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
