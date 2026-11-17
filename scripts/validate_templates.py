from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")


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
        content_lower = path.read_text(encoding="utf-8").lower()
        has_audit_defense = any(
            phrase in content_lower
            for phrase in (
                "evidence would",
                "defend this decision",
                "challenged later",
            )
        )
        has_impact_class = any(
            phrase in content_lower
            for phrase in (
                "affect safety",
                "safety, energization",
                "safety, protection",
                "safety, reliability",
            )
        )
        has_owner_cadence = any(
            phrase in content_lower
            for phrase in (
                "owns the next action",
                "reviewed again",
                "review cadence",
                "accountable owner",
            )
        )
        has_residual_risk = any(
            phrase in content_lower
            for phrase in (
                "residual risk",
                "unresolved risk",
                "accepted risk",
            )
        )
        missing_governance = []
        if not has_audit_defense:
            missing_governance.append("audit-defensibility prompt")
        if not has_impact_class:
            missing_governance.append("safety/risk impact prompt")
        if not has_owner_cadence:
            missing_governance.append("action owner/review prompt")
        if not has_residual_risk:
            missing_governance.append("residual-risk disclosure prompt")
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
