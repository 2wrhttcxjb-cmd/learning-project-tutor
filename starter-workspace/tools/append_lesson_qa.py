#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re


QA_FILE = Path("qa/QA_LOG.md")
QA_ENTRY_RE = re.compile(r"^### QA (\d+)\s*$", re.MULTILINE)
META_KEYWORDS = (
    "实现",
    "脚本",
    "skill",
    "校验",
    "切图",
    "引用失败",
    "manifest",
    "page-",
    "rendered page",
    "状态机",
    "topic_state",
    "branch",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a QA bypass entry to the topic QA log and sync minimal QA state."
    )
    parser.add_argument("topic", help="Topic name, for example YouTube-RCMD")
    parser.add_argument("--question", required=True, help="User QA question text")
    parser.add_argument("--answer", required=True, help="Assistant QA answer text")
    parser.add_argument(
        "--affects-response",
        choices=("yes", "no"),
        default="no",
        help="Whether the QA should influence the formal response interpretation",
    )
    parser.add_argument(
        "--followup-needed",
        choices=("yes", "no"),
        default="no",
        help="Whether this QA exposed a gap that should produce a QA follow-up question",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bypass the QA content guardrail if you have manually verified the QA is valid",
    )
    return parser.parse_args()


def topic_state_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def replace_or_append_yaml_scalar(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*.*$", re.MULTILINE)
    replacement = f"{key}: {value}"
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    if not text.endswith("\n"):
        text += "\n"
    return text + replacement + "\n"


def normalize_block(text: str) -> str:
    stripped = text.rstrip()
    return stripped + "\n"


def looks_meta(question: str, answer: str) -> bool:
    haystack = f"{question}\n{answer}"
    return any(keyword in haystack for keyword in META_KEYWORDS)


def qa_scope_from_state(state_text: str) -> str:
    status = (topic_state_value(state_text, "status") or "").strip()
    lesson_ref = topic_state_value(state_text, "current_lesson_file")

    if status in {"waiting_transfer_response", "ready_for_transfer_diagnosis"}:
        return "Final 02-transfer"
    if status in {"waiting_articulation_response", "ready_for_closure"}:
        return "Final 03-articulation"
    if lesson_ref:
        return f"Lesson {Path(lesson_ref).stem}"
    return "General"


def ensure_scope(text: str, scope: str) -> str:
    header = f"## {scope}"
    if header not in text:
        block = f"\n{header}\n"
        if not text.endswith("\n"):
            text += "\n"
        text += block
    return text


def append_entry_to_scope(text: str, scope: str, entry_block: str) -> tuple[str, int]:
    text = ensure_scope(text, scope)
    header = f"## {scope}"
    before, after = text.split(header, 1)
    after = after.lstrip("\n")
    next_section = re.search(r"^##\s+", after, re.MULTILINE)
    if next_section:
        scope_body = after[: next_section.start()].rstrip()
        trailing = after[next_section.start() :].lstrip("\n")
    else:
        scope_body = after.rstrip()
        trailing = ""

    next_index = 1
    if scope_body:
        matches = list(QA_ENTRY_RE.finditer(scope_body))
        if matches:
            next_index = int(matches[-1].group(1)) + 1

    if scope_body:
        scope_body += "\n\n" + entry_block.rstrip()
    else:
        scope_body = entry_block.rstrip()

    rebuilt = before.rstrip() + "\n\n" + header + "\n\n" + scope_body + "\n"
    if trailing:
        rebuilt += "\n" + trailing.rstrip() + "\n"
    return rebuilt, next_index


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    topic_dir = repo_root / "topics" / args.topic
    if not topic_dir.exists():
        raise SystemExit(f"topic not found: {topic_dir}")

    state_path = topic_dir / "topic_state.yaml"
    if not state_path.exists():
        raise SystemExit(f"topic state not found: {state_path}")
    state_text = read_text(state_path)

    if looks_meta(args.question, args.answer) and not args.force:
        raise SystemExit(
            "Refusing to append likely implementation/debug content into topic QA. "
            "Use --force only after manual verification."
        )

    qa_scope = qa_scope_from_state(state_text)
    qa_path = topic_dir / QA_FILE
    qa_path.parent.mkdir(parents=True, exist_ok=True)

    if qa_path.exists():
        qa_text = read_text(qa_path)
    else:
        qa_text = "# Topic QA Log\n\n"

    entry_template = [
        "### QA {index}",
        f"用户：{args.question}",
        "",
        "回答：",
        args.answer.rstrip(),
        "",
        f"影响正式 response：{args.affects_response}",
    ]
    if args.followup_needed == "yes":
        entry_template.append("需要追加 QA Follow-up：yes")

    updated_text, next_index = append_entry_to_scope(
        normalize_block(qa_text),
        qa_scope,
        "\n".join(entry_template).format(index="{index}"),
    )
    updated_text = updated_text.replace("### QA {index}", f"### QA {next_index}", 1)
    write_text(qa_path, updated_text)

    state_text = replace_or_append_yaml_scalar(state_text, "qa_open", "true")
    state_text = replace_or_append_yaml_scalar(
        state_text, "qa_affects_response", "true" if args.affects_response == "yes" else "false"
    )
    state_text = replace_or_append_yaml_scalar(
        state_text, "qa_followup_needed", "true" if args.followup_needed == "yes" else "false"
    )
    state_text = replace_or_append_yaml_scalar(state_text, "qa_file", str(QA_FILE))
    state_text = replace_or_append_yaml_scalar(state_text, "current_qa_scope", f'"{qa_scope}"')
    state_text = replace_or_append_yaml_scalar(state_text, "current_qa_entry_count", str(next_index))
    state_text = replace_or_append_yaml_scalar(
        state_text, "qa_last_recorded_at", f'"{date.today().isoformat()}"'
    )
    write_text(state_path, state_text)

    print(f"Appended QA {next_index} to {qa_path} [{qa_scope}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
