"""Generate and verify the ARC 500 Fall 2026 local/Git repository release.

Usage from the course workspace root:
    python ARC500_2026_Expanded_Two_Meeting_Materials/release_tools/course_release.py manifest
    python ARC500_2026_Expanded_Two_Meeting_Materials/release_tools/course_release.py sync
    python ARC500_2026_Expanded_Two_Meeting_Materials/release_tools/course_release.py verify
    python ARC500_2026_Expanded_Two_Meeting_Materials/release_tools/course_release.py all

The script never deletes files. If a repository mirror contains stale files,
verification stops and lists them for an explicit, reviewed cleanup.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import zipfile


RELEASE_DATE = "2026-08-20"
PACKAGE_NAME = "ARC500_2026_Expanded_Two_Meeting_Materials"
REPO_PACKAGE = "ARC500_Fall_2026"
MIRROR_DIRS = {
    "Week13_Machine_Learning",
    "Week14_Classification_and_Model_Cards",
    "Week15_Capstone",
}

RELEASE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = RELEASE_ROOT.parent
DEFAULT_BOOK_ROOT = WORKSPACE_ROOT / "Book_Python"

BUILDER_ROOTS = (
    WORKSPACE_ROOT / ".codex_build" / "_design",
    WORKSPACE_ROOT / ".codex_build" / "weeks01_03_expanded",
    WORKSPACE_ROOT / ".codex_build" / "weeks04_08",
    WORKSPACE_ROOT / ".codex_build" / "weeks09_12",
    WORKSPACE_ROOT / ".codex_build" / "weeks13_15",
    WORKSPACE_ROOT / ".codex_build" / "project_templates",
)

SOURCE_SUFFIXES = {
    ".csv",
    ".geojson",
    ".gif",
    ".json",
    ".md",
    ".mjs",
    ".png",
    ".py",
    ".svg",
    ".txt",
    ".yaml",
    ".yml",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def is_transient_release_file(path: Path) -> bool:
    rel = path.relative_to(RELEASE_ROOT)
    return (
        path.name.endswith(".inspect.ndjson")
        or path.suffix.lower() == ".pyc"
        or "__pycache__" in rel.parts
        or path.name in {"course_manifest.yml", "course_manifest.sha256"}
    )


def release_files(*, include_manifest: bool) -> dict[Path, Path]:
    files: dict[Path, Path] = {}
    for path in sorted(RELEASE_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if is_transient_release_file(path):
            if include_manifest and path.name in {"course_manifest.yml", "course_manifest.sha256"}:
                files[path.relative_to(RELEASE_ROOT)] = path
            continue
        files[path.relative_to(RELEASE_ROOT)] = path
    return files


def is_curated_source_file(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    blocked_parts = {"node_modules", "qa", "__pycache__"}
    if any(part in blocked_parts or part.startswith("renders") for part in rel.parts):
        return False
    if path.name.endswith(".inspect.ndjson") or path.suffix.lower() in {".pptx", ".pyc"}:
        return False
    if "montage" in path.name.lower() or path.name.lower() in {"check4.gif"}:
        return False
    return path.suffix.lower() in SOURCE_SUFFIXES


def source_files() -> dict[Path, Path]:
    files: dict[Path, Path] = {}
    codex_root = WORKSPACE_ROOT / ".codex_build"
    for root in BUILDER_ROOTS:
        if not root.exists():
            raise FileNotFoundError(f"Missing builder source root: {root}")
        for path in sorted(root.rglob("*")):
            if path.is_file() and is_curated_source_file(path, root):
                rel = path.relative_to(codex_root)
                files[rel] = path
    return files


def pptx_slide_count(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return sum(
            1
            for name in archive.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        )


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def generate_manifest() -> Path:
    files = release_files(include_manifest=False)
    pptx_paths = [rel for rel in files if rel.suffix.lower() == ".pptx"]
    all_lecture_paths = [rel for rel in pptx_paths if "Template" not in rel.name]
    mirror_paths = [rel for rel in all_lecture_paths if rel.parts and rel.parts[0] in MIRROR_DIRS]
    lecture_paths = [rel for rel in all_lecture_paths if rel not in mirror_paths]
    template_paths = [rel for rel in pptx_paths if "Template" in rel.name]

    lines = [
        "schema_version: 1",
        f"course: {yaml_string('ARC 500 — Programming with Python and Generative AI')}",
        f"release_date: {yaml_string(RELEASE_DATE)}",
        f"package: {yaml_string(PACKAGE_NAME)}",
        "source_deck_policy: "
        + yaml_string(
            "Complete topic-driven source decks; no slide-count cap. "
            "The instructor hides, skips, or shortens slides during delivery."
        ),
        f"lecture_decks: {len(lecture_paths)}",
        f"convenience_mirror_decks: {len(mirror_paths)}",
        f"project_templates: {len(template_paths)}",
        f"powerpoint_files: {len(pptx_paths)}",
        f"distributed_files: {len(files)}",
        "files:",
    ]

    for rel, path in files.items():
        lines.append(f"  - path: {yaml_string(rel.as_posix())}")
        lines.append(f"    bytes: {path.stat().st_size}")
        lines.append(f"    sha256: {yaml_string(sha256(path))}")
        if path.suffix.lower() == ".pptx":
            lines.append(f"    slides: {pptx_slide_count(path)}")

    manifest = RELEASE_ROOT / "course_manifest.yml"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    checksum = RELEASE_ROOT / "course_manifest.sha256"
    checksum.write_text(f"{sha256(manifest)}  course_manifest.yml\n", encoding="ascii")
    print(
        f"manifest: {len(files)} files, {len(lecture_paths)} canonical lecture decks, "
        f"{len(mirror_paths)} convenience mirrors, {len(template_paths)} project templates -> {manifest}"
    )
    return manifest


def checked_repo_paths(book_root: Path) -> tuple[Path, Path, Path]:
    book_root = book_root.resolve()
    expected_git = book_root / ".git"
    if not expected_git.exists():
        raise FileNotFoundError(f"Expected Git repository not found: {expected_git}")
    repo_root = (book_root / "course_materials" / REPO_PACKAGE).resolve()
    try:
        repo_root.relative_to(book_root)
    except ValueError as error:
        raise RuntimeError(f"Unsafe repository release target: {repo_root}") from error
    release_target = repo_root / "release" / PACKAGE_NAME
    source_target = repo_root / "source"
    return repo_root, release_target, source_target


def copy_map(files: dict[Path, Path], target: Path) -> None:
    for rel, source in files.items():
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and sha256(destination) == sha256(source):
            continue
        shutil.copy2(source, destination)


def stale_files(expected: set[Path], target: Path) -> list[Path]:
    if not target.exists():
        return []
    actual = {path.relative_to(target) for path in target.rglob("*") if path.is_file()}
    return sorted(actual - expected)


def sync(book_root: Path) -> None:
    generate_manifest()
    repo_root, release_target, source_target = checked_repo_paths(book_root)
    release_map = release_files(include_manifest=True)
    source_map = source_files()

    release_stale = stale_files(set(release_map), release_target)
    source_stale = stale_files(set(source_map), source_target)
    if release_stale or source_stale:
        print("Refusing to sync over a mirror with stale files; review explicitly:", file=sys.stderr)
        for rel in release_stale:
            print(f"  release/{rel.as_posix()}", file=sys.stderr)
        for rel in source_stale:
            print(f"  source/{rel.as_posix()}", file=sys.stderr)
        raise SystemExit(2)

    copy_map(release_map, release_target)
    copy_map(source_map, source_target)
    print(
        f"synced {len(release_map)} release files and {len(source_map)} authoring files "
        f"to {repo_root}"
    )


def verify_map(files: dict[Path, Path], target: Path, label: str) -> tuple[int, list[str]]:
    failures: list[str] = []
    for rel, source in files.items():
        destination = target / rel
        if not destination.exists():
            failures.append(f"missing {label}: {rel.as_posix()}")
        elif source.stat().st_size != destination.stat().st_size or sha256(source) != sha256(destination):
            failures.append(f"hash mismatch {label}: {rel.as_posix()}")
    for rel in stale_files(set(files), target):
        failures.append(f"stale {label}: {rel.as_posix()}")
    return len(files), failures


def verify(book_root: Path) -> None:
    _, release_target, source_target = checked_repo_paths(book_root)
    release_map = release_files(include_manifest=True)
    source_map = source_files()
    release_count, release_failures = verify_map(release_map, release_target, "release")
    source_count, source_failures = verify_map(source_map, source_target, "source")
    failures = release_failures + source_failures
    if failures:
        print("LOCAL/REPOSITORY PARITY: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        raise SystemExit(1)
    print(
        "LOCAL/REPOSITORY PARITY: PASS — "
        f"{release_count} release files and {source_count} authoring files are byte-identical"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("manifest", "sync", "verify", "all"))
    parser.add_argument("--book-root", type=Path, default=DEFAULT_BOOK_ROOT)
    args = parser.parse_args()

    if args.command == "manifest":
        generate_manifest()
    elif args.command == "sync":
        sync(args.book_root)
    elif args.command == "verify":
        verify(args.book_root)
    else:
        sync(args.book_root)
        verify(args.book_root)


if __name__ == "__main__":
    main()
