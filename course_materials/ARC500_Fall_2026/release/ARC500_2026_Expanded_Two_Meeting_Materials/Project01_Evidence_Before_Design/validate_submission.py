# -*- coding: utf-8 -*-
"""Validate an ARC 500 Project 1 package without executing student code.

Run from the project folder:

    python validate_submission.py .

You may also pass the Submission folder directly. The validator reads files only;
it does not import or execute analysis.py/evidence.py and does not alter the package.
"""

from __future__ import annotations

import argparse
import ast
import math
import struct
import sys
import zipfile
from pathlib import Path

import pandas as pd


REQUIRED_SUMMARY_COLUMNS = ["group", "n", "mean", "median", "outlier_count"]
STATIC_FIGURES = ["figure_01.png", "figure_02.png"]


class Report:
    """Collect readable validation results and determine the process exit code."""

    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def passed(self, message: str) -> None:
        self.passes.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def print(self) -> None:
        for message in self.passes:
            print("PASS ", message)
        for message in self.warnings:
            print("WARN ", message)
        for message in self.failures:
            print("FAIL ", message)
        print()
        print(
            f"Result: {len(self.passes)} pass, {len(self.warnings)} warning, "
            f"{len(self.failures)} failure"
        )


def locate_package(path: Path) -> tuple[Path, Path]:
    """Return (project_root, submission_dir) for a project or Submission path."""
    path = path.resolve()
    if path.name.lower() == "submission":
        return path.parent, path
    if (path / "Submission").is_dir():
        return path, path / "Submission"
    return path, path


def find_file(project: Path, submission: Path, name: str) -> Path | None:
    """Find a file in the expected flattened or supplied-starter locations."""
    candidates = [submission / name, project / name, project / "Starter_Code" / name]
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def parse_python(path: Path, report: Report) -> None:
    """Check syntax and active placeholder nodes without executing untrusted code."""
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as error:
        report.fail(f"{path.name}: Python parse failed -- {error}")
        return

    todo_literals: set[int] = set()
    pass_lines = []

    def record_todo_literals(value: ast.AST | None) -> None:
        if value is None:
            return
        for child in ast.walk(value):
            if (
                isinstance(child, ast.Constant)
                and isinstance(child.value, str)
                and child.value.strip().upper().startswith("TODO")
            ):
                todo_literals.add(child.lineno)

    for node in ast.walk(tree):
        # Flag values a student could submit or display, but not the literal "TODO" used
        # inside a guard such as `if "TODO" in title.upper()`.
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.Return)):
            record_todo_literals(node.value)
        elif isinstance(node, ast.keyword):
            record_todo_literals(node.value)
        elif (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "print"
        ):
            for argument in node.value.args:
                record_todo_literals(argument)
        if isinstance(node, ast.Pass):
            pass_lines.append(node.lineno)

    if todo_literals:
        report.fail(f"{path.name}: active TODO string value(s) at lines {sorted(todo_literals)}")
    if pass_lines:
        report.fail(f"{path.name}: executable pass placeholder(s) at lines {pass_lines}")
    if not todo_literals and not pass_lines:
        report.passed(f"{path.name}: parses and has no active TODO/pass placeholder")


def check_text_file(path: Path | None, label: str, report: Report, *, min_chars: int = 40) -> None:
    if path is None or not path.is_file():
        report.fail(f"{label}: required file is missing")
        return
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        report.fail(f"{label}: cannot read {path.name} -- {error}")
        return
    upper = text.upper()
    placeholder_phrases = (
        "ONE SENTENCE.",
        "COMPLETE ONE LINE PER SUBMITTED COLUMN",
        "STUDENT / PROJECT TITLE",
    )
    lines = text.splitlines()
    blank_fields = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.endswith(":") or len(stripped) > 100:
            continue
        following = next((item.strip() for item in lines[index + 1:] if item.strip()), "")
        next_is_heading = following.startswith(("1. ", "2. ", "3. ", "FINAL "))
        if not following or following.endswith(":") or next_is_heading:
            blank_fields.append(index + 1)

    if len(text.strip()) < min_chars:
        report.fail(f"{label}: {path.name} is too short to be complete")
    elif "TODO" in upper or "REPLACE THIS" in upper or any(phrase in upper for phrase in placeholder_phrases):
        report.fail(f"{label}: {path.name} still contains placeholder text")
    elif blank_fields:
        report.fail(f"{label}: {path.name} has blank field(s) at lines {blank_fields}")
    else:
        report.passed(f"{label}: {path.name}")


def read_image_dimensions(path: Path) -> tuple[int, int]:
    """Read PNG/GIF dimensions with the standard library."""
    with path.open("rb") as handle:
        header = handle.read(24)
    if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
        return struct.unpack(">II", header[16:24])
    if header[:6] in {b"GIF87a", b"GIF89a"} and len(header) >= 10:
        return struct.unpack("<HH", header[6:10])
    raise ValueError("unsupported or corrupt image header")


def check_image(path: Path, label: str, report: Report, minimum: tuple[int, int]) -> None:
    if not path.is_file():
        report.fail(f"{label}: {path.name} is missing")
        return
    try:
        width, height = read_image_dimensions(path)
    except (OSError, ValueError, struct.error) as error:
        report.fail(f"{label}: cannot read dimensions -- {error}")
        return
    if path.stat().st_size < 5_000:
        report.fail(f"{label}: {path.name} is suspiciously small ({path.stat().st_size} bytes)")
    elif width < minimum[0] or height < minimum[1]:
        report.fail(
            f"{label}: {path.name} is {width} x {height}; minimum is {minimum[0]} x {minimum[1]}"
        )
    else:
        report.passed(f"{label}: {path.name} is {width} x {height}")


def check_cleaned_csv(path: Path, report: Report) -> pd.DataFrame | None:
    if not path.is_file():
        report.fail("cleaned_data.csv: required export is missing")
        return None
    try:
        frame = pd.read_csv(path)
    except Exception as error:  # pandas supplies useful parser details
        report.fail(f"cleaned_data.csv: cannot reopen -- {error}")
        return None

    if frame.shape[0] < 2 or frame.shape[1] < 2:
        report.fail(f"cleaned_data.csv: implausible shape {frame.shape}")
    elif any(str(column).startswith("Unnamed:") for column in frame.columns):
        report.fail("cleaned_data.csv: contains an accidental pandas index column")
    elif frame.astype(str).apply(lambda column: column.str.contains("TODO", case=False).any()).any():
        report.fail("cleaned_data.csv: contains placeholder text")
    else:
        report.passed(f"cleaned_data.csv: {frame.shape[0]} rows x {frame.shape[1]} columns")

    required_flags = {"missing_flag", "outlier_flag"}
    if not required_flags.issubset(frame.columns):
        report.fail("cleaned_data.csv: missing_flag and outlier_flag must be separate columns")
    else:
        normalized = {}
        for column in sorted(required_flags):
            values = frame[column]
            if values.dtype == bool:
                normalized[column] = values
            else:
                mapped = values.astype(str).str.strip().str.lower().map({"true": True, "false": False})
                if mapped.isna().any():
                    report.fail(f"cleaned_data.csv: {column} is not consistently Boolean")
                    continue
                normalized[column] = mapped
        if len(normalized) == 2:
            if (normalized["missing_flag"] & normalized["outlier_flag"]).any():
                report.fail("cleaned_data.csv: at least one row is both missing and an outlier")
            else:
                report.passed("cleaned_data.csv: missingness and outlier flags are distinct")
    return frame


def check_summary_csv(path: Path, clean: pd.DataFrame | None, report: Report) -> None:
    if not path.is_file():
        report.fail("grouped_summary.csv: required export is missing")
        return
    try:
        summary = pd.read_csv(path)
    except Exception as error:
        report.fail(f"grouped_summary.csv: cannot reopen -- {error}")
        return

    if list(summary.columns) != REQUIRED_SUMMARY_COLUMNS:
        report.fail(
            "grouped_summary.csv: columns/order must be " + ", ".join(REQUIRED_SUMMARY_COLUMNS)
        )
        return
    if summary.empty or summary["group"].nunique(dropna=False) < 2:
        report.fail("grouped_summary.csv: must contain at least two groups")
        return

    for column in ("n", "mean", "median", "outlier_count"):
        numeric = pd.to_numeric(summary[column], errors="coerce")
        if numeric.isna().any() or not all(math.isfinite(float(value)) for value in numeric):
            report.fail(f"grouped_summary.csv: {column} contains missing/non-finite values")
            return
    if (summary[["n", "outlier_count"]].astype(float) < 0).any().any():
        report.fail("grouped_summary.csv: n/outlier_count cannot be negative")
        return
    if not (summary[["n", "outlier_count"]].astype(float) % 1 == 0).all().all():
        report.fail("grouped_summary.csv: n/outlier_count must be whole numbers")
        return

    if clean is not None:
        if int(summary["n"].sum()) != len(clean):
            report.fail("grouped_summary.csv: n does not account for every cleaned row")
            return
        if "outlier_flag" in clean.columns:
            flags = clean["outlier_flag"]
            if flags.dtype != bool:
                flags = flags.astype(str).str.lower().map({"true": True, "false": False})
            if flags.notna().all() and int(summary["outlier_count"].sum()) != int(flags.sum()):
                report.fail("grouped_summary.csv: outlier_count does not match cleaned row flags")
                return
    report.passed(f"grouped_summary.csv: valid schema and {len(summary)} groups")


def check_outlier_decisions(submission: Path, clean: pd.DataFrame | None, report: Report) -> None:
    """Require one substantive decision record when row-level outlier flags exist."""
    if clean is None or "outlier_flag" not in clean.columns:
        return
    flags = clean["outlier_flag"]
    if flags.dtype != bool:
        flags = flags.astype(str).str.lower().map({"true": True, "false": False})
    if flags.isna().any():
        return
    expected_count = int(flags.sum())
    if expected_count == 0:
        report.passed("outlier decisions: no row is flagged")
        return

    csv_path = submission / "outlier_decisions.csv"
    if csv_path.is_file():
        try:
            decisions = pd.read_csv(csv_path)
        except Exception as error:
            report.fail(f"outlier decisions: cannot reopen outlier_decisions.csv -- {error}")
            return
        required = {"row_index", "action", "reason"}
        if not required.issubset(decisions.columns):
            report.fail("outlier decisions: CSV needs row_index, action, and reason columns")
            return
        allowed = {"KEEP", "INVESTIGATE", "EXCLUDE"}
        actions = decisions["action"].astype(str).str.upper()
        reasons = decisions["reason"].astype(str).str.strip()
        if len(decisions) < expected_count or not actions.isin(allowed).all() or (reasons.str.len() < 20).any():
            report.fail(
                f"outlier decisions: expected at least {expected_count} valid action/reason rows"
            )
        else:
            report.passed(f"outlier decisions: {len(decisions)} valid action/reason rows")
        return

    text_candidates = sorted(submission.glob("*outlier*decision*.txt"))
    if text_candidates:
        check_text_file(text_candidates[0], "outlier decisions", report, min_chars=40 * expected_count)
    else:
        report.fail(
            f"outlier decisions: {expected_count} row(s) are flagged but no CSV/text decision record exists"
        )


def pptx_slide_count(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("ppt/presentation.xml")
    return xml.count(b"<p:sldId ")


def check_pinup(submission: Path, report: Report) -> None:
    decks = sorted(submission.glob("*.pptx"))
    if not decks:
        report.fail("six-slide pin-up: no PPTX found in Submission")
        return
    if len(decks) > 1:
        report.warn(f"six-slide pin-up: multiple PPTX files found; checking {decks[0].name}")
    try:
        count = pptx_slide_count(decks[0])
    except (OSError, KeyError, zipfile.BadZipFile) as error:
        report.fail(f"six-slide pin-up: cannot read {decks[0].name} -- {error}")
        return
    if count != 6:
        report.fail(f"six-slide pin-up: {decks[0].name} contains {count} slides, expected 6")
    else:
        report.passed(f"six-slide pin-up: {decks[0].name} contains 6 slides")


def check_submission(path: Path) -> Report:
    report = Report()
    project, submission = locate_package(path)
    if not submission.is_dir():
        report.fail(f"submission folder does not exist: {submission}")
        return report

    analysis = find_file(project, submission, "analysis.py")
    if analysis is None:
        report.fail("analysis.py: required script is missing")
    else:
        parse_python(analysis, report)
    evidence = find_file(project, submission, "evidence.py")
    if evidence is not None:
        parse_python(evidence, report)
    else:
        report.warn("evidence.py: optional script not found; verify figures are reproducible elsewhere")

    clean = check_cleaned_csv(submission / "cleaned_data.csv", report)
    check_summary_csv(submission / "grouped_summary.csv", clean, report)
    check_outlier_decisions(submission, clean, report)
    check_text_file(submission / "data_dictionary.txt", "data dictionary", report)

    readme_files = [path for path in submission.glob("README*") if "TEMPLATE" not in path.name.upper()]
    check_text_file(readme_files[0] if readme_files else None, "README", report, min_chars=100)
    ai_files = [path for path in submission.glob("*AI*USE*") if "TEMPLATE" not in path.name.upper()]
    check_text_file(ai_files[0] if ai_files else None, "AI-use record", report, min_chars=100)

    for filename in STATIC_FIGURES:
        check_image(submission / filename, filename, report, minimum=(1000, 600))
    extension_candidates = [
        image for image in list(submission.glob("*.png")) + list(submission.glob("*.gif"))
        if image.name not in STATIC_FIGURES
        and any(word in image.stem.lower() for word in ("map", "choropleth", "spatial", "animation"))
    ]
    if not extension_candidates:
        report.fail("extension: no map/choropleth PNG or animation GIF found in Submission")
    else:
        check_image(extension_candidates[0], "extension", report, minimum=(700, 500))

    memo_files = [
        file for suffix in ("*.pdf", "*.docx", "*.txt") for file in submission.glob(suffix)
        if any(word in file.stem.lower() for word in ("memo", "evidence_story", "evidence-memo"))
    ]
    if memo_files:
        memo = memo_files[0]
        if memo.suffix.lower() == ".txt":
            try:
                memo_text = memo.read_text(encoding="utf-8")
                word_count = len(memo_text.split())
            except (OSError, UnicodeError) as error:
                report.fail(f"illustrated memo: cannot read {memo.name} -- {error}")
            else:
                if "TODO" in memo_text.upper() or not 600 <= word_count <= 800:
                    report.fail(
                        f"illustrated memo: {memo.name} has {word_count} words or placeholder text; expected 600-800 words"
                    )
                else:
                    report.passed(f"illustrated memo: {memo.name} has {word_count} words")
        else:
            report.passed(f"illustrated memo: {memo.name} found")
            report.warn("illustrated memo: verify 600-800 words and legibility manually for PDF/DOCX")
    else:
        report.fail("illustrated memo: no memo PDF/DOCX/TXT found in Submission")
    check_pinup(submission, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", type=Path, help="project or Submission folder")
    args = parser.parse_args()
    report = check_submission(args.path)
    report.print()
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main())
