#!/usr/bin/env python3
"""Markdownの資料骨子を別ドキュメント形式へ変換するCLIツール。"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path


HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$")
LIST_PATTERN = re.compile(r"^\s*[-*+]\s+(.*)$")


@dataclass
class Section:
    level: int
    title: str
    bullets: list[str] = field(default_factory=list)


@dataclass
class Outline:
    title: str = "無題"
    sections: list[Section] = field(default_factory=list)


def parse_markdown_outline(content: str) -> Outline:
    outline = Outline()
    current_section: Section | None = None

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        heading_match = HEADING_PATTERN.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            if level == 1 and outline.title == "無題":
                outline.title = title
                current_section = None
                continue
            current_section = Section(level=level, title=title)
            outline.sections.append(current_section)
            continue

        list_match = LIST_PATTERN.match(line)
        if list_match and current_section:
            current_section.bullets.append(list_match.group(1).strip())

    return outline


def render_as_report(outline: Outline) -> str:
    lines: list[str] = [
        f"# {outline.title}（報告書ドラフト）",
        "",
        "## 1. 目的",
        "- 本ドキュメントは骨子から報告書を作成するための下書きです。",
        "",
        "## 2. 要約",
    ]

    for section in outline.sections[:3]:
        lines.append(f"- {section.title}に関する要点をここに記載")

    lines.extend(["", "## 3. 本文"]) 

    for idx, section in enumerate(outline.sections, start=1):
        lines.append("")
        lines.append(f"### 3.{idx} {section.title}")
        if section.bullets:
            lines.extend([f"- {b}" for b in section.bullets])
        else:
            lines.append("- （この節の本文を記載）")

    lines.extend([
        "",
        "## 4. 結論",
        "- 結論の要点を3行で記述",
        "",
        "## 5. 次アクション",
        "- 担当者・期限・成果物を明記",
    ])
    return "\n".join(lines) + "\n"


def render_as_proposal(outline: Outline) -> str:
    lines = [
        f"# {outline.title}（提案書ドラフト）",
        "",
        "## 提案サマリー",
        "- 提案背景：",
        "- 提案内容：",
        "- 期待効果：",
        "",
        "## 現状課題",
    ]

    for section in outline.sections[:4]:
        lines.append(f"- {section.title}")

    lines.append("\n## 解決策")

    for idx, section in enumerate(outline.sections, start=1):
        lines.append("")
        lines.append(f"### 施策{idx}: {section.title}")
        lines.append("- 目的：")
        lines.append("- 実施内容：")
        if section.bullets:
            lines.append("- 実施詳細：")
            lines.extend([f"  - {b}" for b in section.bullets])
        lines.append("- KPI：")

    lines.extend([
        "",
        "## 実行計画",
        "- フェーズ1：",
        "- フェーズ2：",
        "- フェーズ3：",
        "",
        "## 見積・体制",
        "- 概算費用：",
        "- 体制：",
    ])
    return "\n".join(lines) + "\n"


def render_as_minutes(outline: Outline) -> str:
    lines = [
        f"# {outline.title}（議事録テンプレート）",
        "",
        "## 会議情報",
        "- 日時：",
        "- 参加者：",
        "- 目的：",
        "",
        "## 議題",
    ]

    for idx, section in enumerate(outline.sections, start=1):
        lines.append(f"{idx}. {section.title}")

    lines.append("\n## 議論内容")

    for idx, section in enumerate(outline.sections, start=1):
        lines.append("")
        lines.append(f"### 議題{idx}: {section.title}")
        if section.bullets:
            lines.append("- 主な論点：")
            lines.extend([f"  - {b}" for b in section.bullets])
        lines.append("- 決定事項：")
        lines.append("- 懸念事項：")

    lines.extend([
        "",
        "## アクションアイテム",
        "| No | 内容 | 担当 | 期限 |",
        "|---|---|---|---|",
        "| 1 |  |  |  |",
    ])
    return "\n".join(lines) + "\n"


RENDERERS = {
    "report": render_as_report,
    "proposal": render_as_proposal,
    "minutes": render_as_minutes,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Markdown形式の資料骨子を別ドキュメントに変換して出力します。"
    )
    parser.add_argument("input", type=Path, help="入力Markdownファイル")
    parser.add_argument(
        "--style",
        choices=sorted(RENDERERS.keys()),
        default="report",
        help="変換先ドキュメントのスタイル",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="出力先ファイルパス（.md推奨）",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    content = args.input.read_text(encoding="utf-8")
    outline = parse_markdown_outline(content)
    output_text = RENDERERS[args.style](outline)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output_text, encoding="utf-8")
    print(f"Converted: {args.input} -> {args.output} (style={args.style})")


if __name__ == "__main__":
    main()
