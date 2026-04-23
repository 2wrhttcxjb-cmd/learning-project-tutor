#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


QA_ENTRY_RE = re.compile(
    r"^### QA (\d+)\n用户：(.*?)\n\n回答：\n(.*?)\n\n影响正式 response：(yes|no)(?:\n需要追加 QA Follow-up：yes)?$",
    re.MULTILINE | re.DOTALL,
)
DIAGNOSIS_NO_QA_RE = re.compile(r"本课没有记录到 QA")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def topic_state_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def current_scope_from_state(state_text: str) -> str:
    scope = topic_state_value(state_text, "current_qa_scope")
    if scope:
        return scope.strip('"')

    status = (topic_state_value(state_text, "status") or "").strip()
    lesson_ref = topic_state_value(state_text, "current_lesson_file")
    if status in {"waiting_transfer_response", "ready_for_transfer_diagnosis"}:
        return "Final 02-transfer"
    if status in {"waiting_articulation_response", "ready_for_closure"}:
        return "Final 03-articulation"
    if lesson_ref:
        return f"Lesson {Path(lesson_ref).stem}"
    return "General"


def extract_scope_entries(qa_text: str, scope: str) -> list[dict[str, str]]:
    header = f"## {scope}"
    if header not in qa_text:
        return []

    suffix = qa_text.split(header, 1)[1]
    next_section = re.search(r"^##\s+", suffix, re.MULTILINE)
    if next_section:
        suffix = suffix[: next_section.start()]

    entries = []
    for match in QA_ENTRY_RE.finditer(suffix.strip()):
        entries.append(
            {
                "index": match.group(1),
                "question": match.group(2).strip(),
                "answer": match.group(3).strip(),
                "affects_response": match.group(4).strip(),
            }
        )
    return entries


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 tools/validate_lesson_qa.py <topic-name>", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parent.parent
    topic_dir = repo_root / "topics" / sys.argv[1]
    if not topic_dir.exists():
        print(f"Topic not found: {topic_dir}", file=sys.stderr)
        return 1

    state_path = topic_dir / "topic_state.yaml"
    if not state_path.exists():
        print(f"Topic state not found: {state_path}", file=sys.stderr)
        return 1

    state_text = read_text(state_path)
    qa_ref = topic_state_value(state_text, "qa_file") or "qa/QA_LOG.md"
    qa_scope = current_scope_from_state(state_text)
    qa_open = topic_state_value(state_text, "qa_open")
    qa_entry_count = topic_state_value(state_text, "current_qa_entry_count")
    diagnosis_ref = topic_state_value(state_text, "current_diagnosis_file")

    qa_path = topic_dir / qa_ref
    if not qa_path.exists():
        if qa_open == "true":
            print("topic_state.qa_open is true but qa_file does not exist")
            return 2
        print(f"Topic QA validated for {topic_dir.name}")
        return 0

    entries = extract_scope_entries(read_text(qa_path), qa_scope)
    errors: list[str] = []

    if entries:
        if qa_open != "true":
            errors.append("qa_file has entries for current scope but topic_state.qa_open is not true")
        try:
            expected_count = int(qa_entry_count or "0")
        except ValueError:
            expected_count = -1
        if expected_count != len(entries):
            errors.append(
                f"topic_state current_qa_entry_count={qa_entry_count} but current QA scope has {len(entries)} entries"
            )
    elif qa_open == "true":
        errors.append("topic_state.qa_open is true but current QA scope has no entries")

    if diagnosis_ref:
        diagnosis_path = topic_dir / diagnosis_ref
        if diagnosis_path.exists():
            diagnosis_text = read_text(diagnosis_path)
            if entries and DIAGNOSIS_NO_QA_RE.search(diagnosis_text):
                errors.append("diagnosis says no QA exists, but current QA scope has entries")

    if errors:
        for error in errors:
            print(error)
        return 2

    print(f"Topic QA validated for {topic_dir.name} [{qa_scope}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
