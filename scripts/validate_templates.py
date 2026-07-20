from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip()[1:-1].split("|")]


def table_blocks(lines: list[str]) -> list[tuple[int, list[str]]]:
    blocks: list[tuple[int, list[str]]] = []
    index = 0
    while index < len(lines):
        if not is_table_row(lines[index]):
            index += 1
            continue

        start = index
        block: list[str] = []
        while index < len(lines) and is_table_row(lines[index]):
            block.append(lines[index])
            index += 1
        blocks.append((start + 1, block))
    return blocks


def validate_template(path: Path) -> list[tuple[int, str]]:
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

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate structural conventions in BESS Markdown templates."
    )
    parser.add_argument("paths", nargs="*", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = args.paths or sorted(Path("templates").glob("*.md"))
    if not paths:
        print("No templates found.", file=sys.stderr)
        return 1

    error_count = 0
    for path in paths:
        for line, message in validate_template(path):
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
