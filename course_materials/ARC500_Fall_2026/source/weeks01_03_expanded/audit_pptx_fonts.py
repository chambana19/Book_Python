from __future__ import annotations

import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "ARC500_2026_Expanded_Two_Meeting_Materials" / "Weeks01-03_Foundations"
DECKS = [
    "ARC500_Week01A_Computational_Thinking_and_Responsible_AI.pptx",
    "ARC500_Week01B_Spyder_Installation_and_First_Program.pptx",
    "ARC500_Week02A_Values_Variables_Units_and_Expressions.pptx",
    "ARC500_Week02B_Spyder_Architectural_Quantity_Studio.pptx",
    "ARC500_Week03A_Asynchronous_Decisions_and_Functions_Primer.pptx",
    "ARC500_Week03B_Spyder_Design_Rule_and_Function_Studio.pptx",
]


def main() -> None:
    for name in DECKS:
        path = OUT / name
        with zipfile.ZipFile(path) as archive:
            slide_names = sorted(n for n in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n))
            note_names = sorted(n for n in archive.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n))
            sizes: list[int] = []
            auto_fit = 0
            for member in slide_names:
                text = archive.read(member).decode("utf-8", errors="ignore")
                sizes.extend(int(value) for value in re.findall(r'\bsz="(\d+)"', text))
                auto_fit += text.count("<a:normAutofit") + text.count("<a:spAutoFit")
            fractional = [value for value in sizes if value % 100]
            if fractional:
                raise AssertionError(f"{name}: non-integer point sizes {sorted(set(fractional))}")
            if auto_fit:
                raise AssertionError(f"{name}: contains {auto_fit} auto-fit directives")
            point_sizes = sorted(set(value // 100 for value in sizes))
            print(f"{name}: {len(slide_names)} slides; {len(note_names)} notes; integer sizes={point_sizes}; auto-fit=0")


if __name__ == "__main__":
    main()
