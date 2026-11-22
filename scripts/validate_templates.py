from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")
CODE_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
CLOSEOUT_HEADINGS = {"## closeout questions", "## closeout prompts"}
CLOSEOUT_QUESTIONS = {
    "audit-defensibility prompt": r"what evidence would .*(?:audit|challenged later)\?",
    "safety/risk impact prompt": (
        r"does the (?:finding|item) affect safety, energization, warranty, "
        r"grid compliance, or (?:only )?documentation(?: quality)?\?"
    ),
    "action owner/review prompt": r"who owns the next action.*when .*review.*\?",
    "residual-risk disclosure prompt": (
        r"(?:what|which) (?:unresolved (?:residual )?|residual )risk "
        r".*final acceptance package\?"
    ),
}


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return False
    slashes = len(stripped[:-1]) - len(stripped[:-1].rstrip("\\"))
    return slashes % 2 == 0


def table_cells(line: str) -> list[str]:
    content = line.strip()
    if content.startswith("|"):
        content = content[1:]
    if content.endswith("|"):
        slashes = len(content[:-1]) - len(content[:-1].rstrip("\\"))
        if slashes % 2 == 0:
            content = content[:-1]

    cells: list[str] = []
    current: list[str] = []
    escape_count = 0
    for char in content:
        if char == "\\":
            escape_count += 1
            current.append(char)
        elif char == "|":
            if escape_count % 2 == 1:
                current.append(char)
            else:
                cells.append("".join(current).strip())
                current = []
            escape_count = 0
        else:
            escape_count = 0
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def table_blocks(
    lines: list[str], *, strict: bool = False
) -> list[tuple[int, list[str]]]:
    visible_lines = _visible_markdown_lines(lines)
    blocks: list[tuple[int, list[str]]] = []
    index = 0
    while index < len(visible_lines):
        if not is_table_row(visible_lines[index]):
            index += 1
            continue

        start = index
        block: list[str] = []
        while index < len(visible_lines) and is_table_row(visible_lines[index]):
            block.append(visible_lines[index])
            index += 1
        if strict:
            header = table_cells(block[0])
            separator = table_cells(block[1]) if len(block) > 1 else []
            if len(separator) != len(header) or any(
                not SEPARATOR_CELL.fullmatch(cell) for cell in separator
            ):
                raise ValueError(
                    f"line {start + 2}: table separator must match the header "
                    "width and use at least three dashes"
                )
        blocks.append((start + 1, block))
    return blocks


def _strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    visible: list[str] = []
    while line:
        if in_comment:
            _, marker, line = line.partition("-->")
            in_comment = not marker
        else:
            text, marker, line = line.partition("<!--")
            visible.append(text)
            in_comment = bool(marker)
    return "".join(visible), in_comment


def _visible_markdown_lines(lines: list[str]) -> list[str]:
    """Blank fenced code and HTML comments without changing source line numbers."""

    visible_lines: list[str] = []
    fence_character = ""
    fence_length = 0
    in_comment = False
    for line in lines:
        if fence_character:
            marker = CODE_FENCE.match(line)
            if (
                marker
                and marker[1][0] == fence_character
                and len(marker[1]) >= fence_length
                and not marker[2].strip()
            ):
                fence_character = ""
                fence_length = 0
            visible_lines.append("")
            continue

        line, in_comment = _strip_html_comments(line, in_comment)
        marker = CODE_FENCE.match(line)
        if marker:
            fence_character = marker[1][0]
            fence_length = len(marker[1])
            visible_lines.append("")
        else:
            visible_lines.append(line)
    return visible_lines


def _closeout_questions(lines: list[str]) -> list[str]:
    questions: list[str] = []
    in_closeout = False
    fence = ""
    in_comment = False
    for line in lines:
        marker = CODE_FENCE.match(line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = ""
            continue
        if marker and not in_comment:
            fence = marker[1]
            continue
        line, in_comment = _strip_html_comments(line, in_comment)
        if line.startswith(("# ", "## ")):
            in_closeout = line.rstrip().casefold() in CLOSEOUT_HEADINGS
        elif in_closeout and line.startswith(("- ", "* ", "+ ")):
            questions.append(line[2:].strip().casefold())
    return questions


def validate_template(
    path: Path, *, strict_governance: bool = False
) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[tuple[int, str]] = []
    nonempty = [(index, line) for index, line in enumerate(lines) if line.strip()]

    if not nonempty:
        return [(1, "template is empty")]

    first_index, first_line = nonempty[0]
    if not first_line.startswith("# "):
        errors.append((first_index + 1, "first content line must be an H1 title"))

    h1_lines = [index for index, line in enumerate(lines) if line.startswith("# ")]
    if len(h1_lines) != 1:
        errors.append((1, f"expected exactly one H1 title, found {len(h1_lines)}"))

    if h1_lines:
        intro_line = next(
            (
                (index, lines[index].strip())
                for index in range(h1_lines[0] + 1, len(lines))
                if lines[index].strip()
            ),
            None,
        )
        if intro_line is None:
            errors.append((h1_lines[0] + 1, "template needs an introductory paragraph"))
        else:
            index, content = intro_line
            if content.startswith(("#", "|", "- ", "* ", "```")):
                errors.append(
                    (
                        index + 1,
                        "add an introductory paragraph before structured content",
                    )
                )

    blocks = table_blocks(lines)
    if not blocks:
        errors.append((1, "template must contain at least one Markdown table"))

    for start_line, block in blocks:
        if len(block) < 3:
            errors.append(
                (start_line, "table must include a header, separator, and data row")
            )
            continue

        header = table_cells(block[0])
        separator = table_cells(block[1])
        if not header or any(not cell for cell in header):
            errors.append((start_line, "table header cells must not be empty"))

        if len(separator) != len(header) or any(
            not SEPARATOR_CELL.fullmatch(cell) for cell in separator
        ):
            errors.append(
                (
                    start_line + 1,
                    "table separator must match the header width and use at "
                    "least three dashes",
                )
            )

        for offset, row in enumerate(block[2:], start=2):
            cells = table_cells(row)
            if len(cells) != len(header):
                errors.append(
                    (
                        start_line + offset,
                        f"table row has {len(cells)} cells; expected {len(header)}",
                    )
                )

    if strict_governance:
        questions = _closeout_questions(lines)
        missing_governance = [
            label
            for label, pattern in CLOSEOUT_QUESTIONS.items()
            if not any(re.fullmatch(pattern, question) for question in questions)
        ]
        if missing_governance:
            errors.append(
                (
                    1,
                    "strict governance requires closeout defensibility prompts: "
                    + ", ".join(missing_governance),
                )
            )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate structural conventions in BESS Markdown templates."
    )
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument(
        "--strict-governance",
        action="store_true",
        help="Enforce mandatory closeout defensibility prompts in templates.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = args.paths or sorted(Path("templates").glob("*.md"))
    if not paths:
        print("No templates found.", file=sys.stderr)
        return 1

    error_count = 0
    for path in paths:
        for line, message in validate_template(
            path, strict_governance=args.strict_governance
        ):
            print(f"{path}:{line}: {message}", file=sys.stderr)
            error_count += 1

    if error_count:
        print(
            f"Template validation failed with {error_count} error(s).",
            file=sys.stderr,
        )
        return 1

    print(f"Validated {len(paths)} template(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
