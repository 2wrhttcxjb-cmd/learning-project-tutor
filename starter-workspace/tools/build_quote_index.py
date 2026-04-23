#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


MARKER_RE = re.compile(
    r"^%%(?:QUOTE(?::\s*(.*?))?|fav(?::\s*(.*?))?)%%\s*$",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


@dataclass
class QuoteEntry:
    file_path: Path
    heading: str | None
    block_type: str
    excerpt: str
    source_ref: str | None
    note: str | None


def relative_to_topic(path: Path, topic_dir: Path) -> str:
    return str(path.relative_to(topic_dir)).replace("\\", "/")


def extract_block(lines: list[str], marker_index: int) -> tuple[list[str], int]:
    i = marker_index - 1
    while i >= 0 and not lines[i].strip():
        i -= 1
    end = i
    while i >= 0 and lines[i].strip():
        i -= 1
    start = i + 1
    return lines[start : end + 1], start


def find_heading(lines: list[str], block_start: int) -> str | None:
    for i in range(block_start, -1, -1):
        m = HEADING_RE.match(lines[i])
        if m:
            return m.group(2).strip()
    return None


def classify_block(block_lines: list[str]) -> tuple[str, str, str | None]:
    block_text = "\n".join(block_lines).strip()
    source_ref = None
    block_type = "Quote"

    if any(line.startswith("> [Paper Quote]") for line in block_lines):
        block_type = "Paper Quote"
    elif any(line.startswith("> [Paper Figure]") for line in block_lines):
        block_type = "Paper Figure"
    elif any(line.startswith("回答：") for line in block_lines):
        block_type = "QA Answer"
    elif any(line.startswith("用户：") for line in block_lines):
        block_type = "QA Question"
    else:
        block_type = "Lesson Note"

    for line in block_lines:
        stripped = line.strip()
        if stripped.startswith("> Source:"):
            source_ref = stripped.removeprefix("> Source:").strip()
            break
        if stripped.startswith("Source:"):
            source_ref = stripped.removeprefix("Source:").strip()
            break

    excerpt_lines: list[str] = []
    for line in block_lines:
        stripped = line.strip()
        if stripped.startswith("> [Paper Quote]") or stripped.startswith("> [Paper Figure]"):
            continue
        if stripped.startswith("> Source:") or stripped.startswith("Source:"):
            continue
        if stripped.startswith("> "):
            stripped = stripped[2:]
        excerpt_lines.append(stripped)

    excerpt = " ".join(part for part in excerpt_lines if part).strip()
    excerpt = re.sub(r"\s+", " ", excerpt)
    if len(excerpt) > 180:
        excerpt = excerpt[:177].rstrip() + "..."

    return block_type, excerpt or block_text[:180], source_ref


def collect_entries(topic_dir: Path) -> list[QuoteEntry]:
    entries: list[QuoteEntry] = []
    root = topic_dir / "lessons"
    if not root.exists():
        return entries
    for path in sorted(root.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(lines):
            m = MARKER_RE.match(line)
            if not m:
                continue
            raw_note = m.group(1) if m.group(1) is not None else m.group(2)
            note = raw_note.strip() if raw_note and raw_note.strip() else None
            block_lines, block_start = extract_block(lines, idx)
            heading = find_heading(lines, block_start)
            block_type, excerpt, source_ref = classify_block(block_lines)
            entries.append(
                QuoteEntry(
                    file_path=path,
                    heading=heading,
                    block_type=block_type,
                    excerpt=excerpt,
                    source_ref=source_ref,
                    note=note,
                )
            )
    return entries


def render_index(topic_dir: Path, entries: list[QuoteEntry]) -> str:
    topic_name = topic_dir.name
    lines: list[str] = [
        "# Quote Index",
        "",
        f"## Topic",
        topic_name,
        "",
        "## How to mark quotes",
        "在 `lessons/` 里的任意一段 quote / figure /解释段落下面，单独加一行：",
        "",
        "```md",
        "%%fav: %%",
        "```",
        "",
        "也可以写备注：",
        "",
        "```md",
        "%%fav: 这句适合以后复习因果链%%",
        "```",
        "",
        "运行 `python3 tools/build_quote_index.py <topic-name>` 后，这个索引会被刷新。",
        "",
        "## Saved Quotes",
        "",
    ]

    if not entries:
        lines.extend(
            [
                "当前还没有标记的 quote。",
                "",
                "你可以先在 lesson 或 QA 文件里用 `%%fav: %%` 标出想保留的内容，再刷新索引。",
            ]
        )
        return "\n".join(lines) + "\n"

    for entry in entries:
        rel = relative_to_topic(entry.file_path, topic_dir)
        heading = entry.heading or Path(rel).stem
        link = f"[[{rel}#{heading}|{rel} · {heading}]]"
        lines.append(f"- `{entry.block_type}` {link}")
        lines.append(f"  摘录：{entry.excerpt}")
        if entry.source_ref:
            lines.append(f"  原文定位：{entry.source_ref}")
        if entry.note:
            lines.append(f"  备注：{entry.note}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 tools/build_quote_index.py <topic-name>", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parent.parent
    topic_dir = repo_root / "topics" / sys.argv[1]
    if not topic_dir.exists():
        print(f"Topic not found: {topic_dir}", file=sys.stderr)
        return 1

    entries = collect_entries(topic_dir)
    quotes_dir = topic_dir / "quotes"
    quotes_dir.mkdir(parents=True, exist_ok=True)
    out_path = quotes_dir / "QUOTE_INDEX.md"
    out_path.write_text(render_index(topic_dir, entries), encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
