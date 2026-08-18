"""Generate reproducible teaching diagrams and Matplotlib result figures.

Run from the repository root:
    python scripts/generate_book_figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np
import pandas as pd


OUTPUT = Path("Figures/Generated")
OUTPUT.mkdir(parents=True, exist_ok=True)

BLUE = "#2E6FBB"
ORANGE = "#E68619"
GREEN = "#3A9158"
PURPLE = "#7554A3"
DARK = "#263248"
MID = "#D9E3F0"

# Explanatory box-and-arrow diagrams are strictly monochrome: black outline on
# white fill by default, inverted to black fill with white text for the one
# box a diagram exists to highlight. Chart-style figures keep the separate
# tab:blue/orange/green data-series palette defined above.
INK = "#000000"
PAPER = "#FFFFFF"
MUTED = "#4D4D4D"
HILITE_SUBTITLE = "#E6E6E6"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "axes.edgecolor": DARK,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
    }
)


def save(fig: plt.Figure, stem: str) -> None:
    """Save a compact vector copy for LaTeX and a PNG for quick preview."""
    fig.savefig(OUTPUT / f"{stem}.pdf", bbox_inches="tight", facecolor="white")
    fig.savefig(
        OUTPUT / f"{stem}.png",
        dpi=180,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)


def blank_canvas(width: float = 10, height: float = 4) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(width, height), layout="constrained")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def rounded_box(ax, xy, width, height, text, fontsize=11, subtitle=None, fill=False):
    """A black-outline, white-fill box. Set fill=True to invert it (black
    fill, white text) for the single box a diagram exists to highlight."""
    x, y = xy
    face_color = INK if fill else PAPER
    title_color = PAPER if fill else INK
    subtitle_color = HILITE_SUBTITLE if fill else MUTED
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        # boxstyle's "pad" visually expands the rendered outline this far
        # beyond the (x, y, width, height) given, on every side -- confirmed
        # empirically via patch.get_extents(). At the old pad=0.012 that is
        # ~9.5pt on an 11in-wide figure, which is *larger* than arrow()'s
        # shrink and was the real cause of arrows rendering as touching or
        # overlapping the outline even when their coordinates looked fine.
        # Every box here is already sized with deliberate internal margin
        # around its centered text, so this expansion is pure unwanted
        # padding; kept small (not zero) only to preserve the rounded-corner
        # look at this box scale.
        boxstyle="round,pad=0.003,rounding_size=0.02",
        linewidth=1.4,
        edgecolor=INK,
        facecolor=face_color,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + height * (0.57 if subtitle else 0.5),
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        weight="bold",
        color=title_color,
    )
    if subtitle:
        ax.text(
            x + width / 2,
            y + height * 0.27,
            subtitle,
            ha="center",
            va="center",
            fontsize=8.5,
            color=subtitle_color,
        )
    return patch


def arrow(ax, start, end, connectionstyle="arc3", linestyle="-", shrink=9):
    """A black arrow. Use linestyle="--" for the secondary path of a genuine
    two-outcome branch (the primary/expected path stays solid).

    `shrink` (points) pulls both the tail and head back *along the arrow's
    own direction* from the exact coordinates given. For an arrow that meets
    a box edge head-on this becomes a clean perpendicular gap; for a
    diagonal arrow meeting an edge at a shallow angle, the perpendicular
    component falls off with the sine of that angle and can round to
    nothing, so those cases also need a small manual offset baked into the
    coordinates (see the style guide). Either way, `shrink` must exceed
    rounded_box()'s ~2.4pt pad expansion (at pad=0.003, 11in-wide figure)
    just to reach the box's true rendered edge before it can clear it; the
    default leaves roughly 6.6pt of real gap while still safely fitting the
    shortest arrows in the book (~36pt end to end)."""
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.4,
            color=INK,
            linestyle=linestyle,
            connectionstyle=connectionstyle,
            shrinkA=shrink,
            shrinkB=shrink,
        )
    )


def generate_workflow_diagram() -> None:
    fig, ax = blank_canvas(11, 4.3)
    ax.text(
        0.5,
        0.93,
        "The edit-run-read-revise learning loop",
        ha="center",
        va="center",
        fontsize=16,
        weight="bold",
        color=DARK,
    )
    labels = [
        ("1. Edit", "Change one idea"),
        ("2. Save", "Write the file"),
        ("3. Run", "Ask Python"),
        ("4. Read", "Output or error"),
        ("5. Revise", "Explain and improve"),
    ]
    xs = np.linspace(0.04, 0.8, len(labels))
    for x, (title, subtitle) in zip(xs, labels):
        rounded_box(ax, (x, 0.38), 0.14, 0.28, title, subtitle=subtitle)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, (left + 0.14, 0.52), (right, 0.52))
    arrow(
        ax,
        (0.88, 0.34),
        (0.12, 0.33),
        connectionstyle="arc3,rad=-0.13",
        linestyle="--",
    )
    ax.text(0.5, 0.29, "loop back and revise", ha="center", color=DARK, fontsize=9, weight="bold")
    ax.text(
        0.5,
        0.03,
        "A surprising result is information: compare it with your prediction, then change one thing.",
        ha="center",
        color="#52647C",
        fontsize=10,
    )
    save(fig, "ch01_edit_run_loop")


def generate_function_anatomy() -> None:
    fig, ax = blank_canvas(11, 4.1)
    ax.text(
        0.5,
        0.93,
        "A function connects inputs, a process, and one returned result",
        ha="center",
        fontsize=15,
        weight="bold",
        color=DARK,
    )
    rounded_box(ax, (0.04, 0.37), 0.21, 0.32, "Arguments", subtitle="width=10.5, depth=20.0")
    rounded_box(ax, (0.36, 0.24), 0.30, 0.55, "calculate_area(width, depth)", subtitle="area = width * depth\nreturn area")
    rounded_box(ax, (0.77, 0.37), 0.19, 0.32, "Return value", subtitle="210.0")
    arrow(ax, (0.25, 0.53), (0.36, 0.53))
    arrow(ax, (0.66, 0.53), (0.77, 0.53))
    ax.text(0.305, 0.59, "bind to\nparameters", ha="center", color=MUTED, fontsize=9)
    ax.text(0.715, 0.59, "send back to\ncaller", ha="center", color=MUTED, fontsize=9)
    ax.text(
        0.5,
        0.10,
        "Define once -> call many times. Printing shows a value; returning lets later code use it.",
        ha="center",
        fontsize=10,
        color="#52647C",
    )
    save(fig, "ch06_function_anatomy")


def generate_builtin_toolbox() -> None:
    fig, ax = blank_canvas(10.5, 5.0)
    ax.text(0.5, 0.94, "Choose a built-in function from the task", ha="center", fontsize=16, weight="bold", color=DARK)
    groups = [
        ("Measure", "len(), min(), max(), sum()"),
        ("Reorder", "sorted(), reversed()"),
        ("Decide", "any(), all()"),
        ("Pair", "enumerate(), zip()"),
        ("Convert", "int(), float(), str(), list()"),
        ("Inspect", "type(), help()"),
    ]
    positions = [(0.06, 0.58), (0.37, 0.58), (0.68, 0.58), (0.06, 0.22), (0.37, 0.22), (0.68, 0.22)]
    for (title, functions), position in zip(groups, positions):
        rounded_box(ax, position, 0.26, 0.22, title, subtitle=functions)
    ax.text(
        0.5,
        0.07,
        "Ask what operation the program needs before choosing a function name.",
        ha="center",
        color="#52647C",
    )
    save(fig, "ch07_builtin_toolbox")


def generate_traceback_anatomy() -> None:
    fig, ax = blank_canvas(10.5, 4.8)
    ax.text(0.5, 0.94, "Read a traceback from the bottom upward", ha="center", fontsize=16, weight="bold", color=DARK)
    rows = [
        (0.68, "Where Python was running", 'File "room_check.py", line 8, in <module>'),
        (0.45, "The instruction that failed", "area = width * depth"),
        (0.22, "Error type and message", "TypeError: can't multiply sequence by non-int"),
    ]
    for y, title, code in rows:
        rounded_box(ax, (0.16, y), 0.68, 0.15, title, subtitle=code)
    arrow(ax, (0.09, 0.27), (0.09, 0.75))
    ax.text(0.06, 0.50, "read upward", rotation=90, ha="center", va="center", color=DARK, weight="bold")
    ax.text(0.5, 0.07, "Start with the last line: it names the problem. Then locate the failing instruction.", ha="center", color="#52647C")
    save(fig, "ch08_traceback_anatomy")


def generate_copying_models() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.2), layout="constrained")
    fig.suptitle("Assignment, shallow copy, and deep copy", fontsize=16, weight="bold", color=DARK)
    titles = ["Assignment", "Shallow copy", "Deep copy"]
    subtitles = ["Two names, one object", "New outer object, shared nested object", "Independent nested objects"]
    for ax, title, subtitle in zip(axes, titles, subtitles):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title(title, color=DARK, weight="bold")
        ax.text(0.5, 0.88, subtitle, ha="center", fontsize=8.5, color="#52647C")

    # Solid arrows track "a"; dashed arrows track "b", consistently in every panel.
    # Assignment
    rounded_box(axes[0], (0.06, 0.57), 0.25, 0.14, "a")
    rounded_box(axes[0], (0.06, 0.30), 0.25, 0.14, "b")
    rounded_box(axes[0], (0.62, 0.40), 0.30, 0.25, "outer list", subtitle="nested list")
    arrow(axes[0], (0.31, 0.64), (0.62, 0.57))
    arrow(axes[0], (0.31, 0.37), (0.62, 0.49), linestyle="--")

    # Shallow copy
    rounded_box(axes[1], (0.05, 0.50), 0.27, 0.18, "a outer")
    rounded_box(axes[1], (0.05, 0.22), 0.27, 0.18, "b outer")
    rounded_box(axes[1], (0.47, 0.35), 0.50, 0.20, "shared nested", fontsize=10, fill=True)
    arrow(axes[1], (0.32, 0.59), (0.47, 0.48))
    arrow(axes[1], (0.32, 0.31), (0.47, 0.42), linestyle="--")

    # Deep copy
    rounded_box(axes[2], (0.05, 0.53), 0.27, 0.18, "a outer")
    rounded_box(axes[2], (0.05, 0.20), 0.27, 0.18, "b outer")
    rounded_box(axes[2], (0.64, 0.53), 0.34, 0.18, "nested A")
    rounded_box(axes[2], (0.64, 0.20), 0.34, 0.18, "nested B")
    arrow(axes[2], (0.32, 0.62), (0.64, 0.62))
    arrow(axes[2], (0.32, 0.29), (0.64, 0.29), linestyle="--")
    save(fig, "ch09_copying_models")


def generate_file_pipeline() -> None:
    fig, ax = blank_canvas(11, 4.0)
    ax.text(0.5, 0.93, "A safe file operation is a short pipeline", ha="center", fontsize=16, weight="bold", color=DARK)
    steps = [
        ("Path", 'Path("rooms.csv")'),
        ("Mode", '"r", "w", or "a"'),
        ("Context", "with ... as file"),
        ("Operation", "read / write / parse"),
        ("Result", "closed file + data"),
    ]
    xs = np.linspace(0.03, 0.81, len(steps))
    for x, (title, subtitle) in zip(xs, steps):
        rounded_box(ax, (x, 0.39), 0.14, 0.28, title, subtitle=subtitle)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, (left + 0.14, 0.53), (right, 0.53))
    ax.text(0.5, 0.17, "The with block closes the file even when an exception interrupts the operation.", ha="center", color="#52647C")
    save(fig, "ch10_file_pipeline")


def generate_array_axes() -> None:
    fig, ax = blank_canvas(9.5, 5.1)
    ax.text(0.5, 0.95, "Rows, columns, and NumPy axes", ha="center", fontsize=16, weight="bold", color=DARK)
    values = np.array([[12, 16, 14], [10, 15, 13], [11, 17, 15]])
    x0, y0, cell = 0.26, 0.25, 0.15
    for row in range(3):
        for col in range(3):
            x = x0 + col * cell
            y = y0 + (2 - row) * cell
            ax.add_patch(Rectangle((x, y), cell, cell, facecolor=PAPER, edgecolor=INK, linewidth=1.3))
            ax.text(x + cell / 2, y + cell / 2, str(values[row, col]), ha="center", va="center", fontsize=13, color=DARK)
    ax.text(x0 + 1.5 * cell, 0.79, "columns", ha="center", weight="bold", color=DARK)
    ax.text(0.16, y0 + 1.5 * cell, "rows", ha="center", va="center", rotation=90, weight="bold", color=DARK)
    arrow(ax, (0.75, 0.72), (0.75, 0.28))
    ax.text(0.78, 0.50, "axis=0\noperate down rows\n-> one result per column", va="center", color=DARK, fontsize=10)
    arrow(ax, (0.25, 0.13), (0.70, 0.13), linestyle="--")
    ax.text(0.48, 0.05, "axis=1: operate across columns -> one result per row", ha="center", color=DARK, fontsize=10)
    save(fig, "ch11_array_axes")


def generate_dataframe_pipeline() -> None:
    fig, ax = blank_canvas(11, 4.3)
    ax.text(0.5, 0.94, "A readable pandas analysis separates stages", ha="center", fontsize=16, weight="bold", color=DARK)
    steps = [
        ("Load", "CSV or dictionary"),
        ("Inspect", "head, info, dtypes"),
        ("Clean", "missing values"),
        ("Transform", "filter, assign, group"),
        ("Communicate", "table, chart, export"),
    ]
    xs = np.linspace(0.03, 0.81, len(steps))
    for x, (title, subtitle) in zip(xs, steps):
        rounded_box(ax, (x, 0.45), 0.14, 0.25, title, subtitle=subtitle)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, (left + 0.14, 0.575), (right, 0.575))
    table_data = [["room", "area_m2"], ["Lobby", "24.0"], ["Office", "18.0"], ["Cafe", "31.0"]]
    table = ax.table(cellText=table_data, cellLoc="center", bbox=[0.32, 0.06, 0.36, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    for (row, _col), cell_obj in table.get_celld().items():
        cell_obj.set_edgecolor(MID)
        cell_obj.set_facecolor("#E8F2FC" if row == 0 else "white")
        if row == 0:
            cell_obj.set_text_props(weight="bold", color=DARK)
    save(fig, "ch12_dataframe_pipeline")


def generate_program_pipeline() -> None:
    fig, ax = blank_canvas(11, 3.8)
    ax.text(0.5, 0.93, "What happens when a Python program runs", ha="center", fontsize=16, weight="bold", color=DARK)
    steps = [
        ("Source code", "instructions in a .py file"),
        ("Python interpreter", "reads syntax in order"),
        ("Program state", "values bound to names"),
        ("Observable result", "output, file, plot, or error"),
    ]
    xs = [0.03, 0.28, 0.53, 0.78]
    for x, (title, subtitle) in zip(xs, steps):
        rounded_box(ax, (x, 0.38), 0.19, 0.30, title, subtitle=subtitle)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, (left + 0.19, 0.53), (right, 0.53))
    ax.text(0.5, 0.15, "A program is a sequence of state changes; the screen shows only the observable effects.", ha="center", color="#52647C")
    save(fig, "ch01_program_pipeline")


def generate_expression_trace() -> None:
    fig, ax = blank_canvas(11, 4.0)
    ax.text(0.5, 0.94, "Trace an expression one transformation at a time", ha="center", fontsize=16, weight="bold", color=DARK)
    steps = [
        ("Expression", "width * height"),
        ("Substitute names", "3.0 * 4.0"),
        ("Apply operator", "12.0"),
        ("Bind result", "area = 12.0 (float)"),
    ]
    xs = [0.03, 0.28, 0.53, 0.78]
    for x, (title, subtitle) in zip(xs, steps):
        rounded_box(ax, (x, 0.39), 0.19, 0.30, title, subtitle=subtitle)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, (left + 0.19, 0.54), (right, 0.54))
    ax.text(0.5, 0.15, "The equals sign stores the value produced on its right; it does not assert a permanent equation.", ha="center", color="#52647C")
    save(fig, "ch02_expression_trace")


def generate_decision_trace() -> None:
    fig, ax = blank_canvas(10.5, 5.2)
    ax.text(0.5, 0.95, "A conditional selects exactly one path", ha="center", fontsize=16, weight="bold", color=DARK)
    rounded_box(ax, (0.34, 0.68), 0.32, 0.16, "18 <= temperature_c <= 24?")
    rounded_box(ax, (0.08, 0.31), 0.30, 0.18, "True branch", subtitle='status = "comfortable"')
    rounded_box(ax, (0.62, 0.31), 0.30, 0.18, "False branch", subtitle='status = "check conditions"')
    rounded_box(ax, (0.34, 0.07), 0.32, 0.14, "Continue after the if statement")
    label_box = dict(facecolor="white", edgecolor="none", pad=1.5)
    arrow(ax, (0.40, 0.666), (0.24, 0.504))
    arrow(ax, (0.60, 0.666), (0.76, 0.504), linestyle="--")
    ax.text(0.30, 0.685, "True", color=DARK, weight="bold", fontsize=10, ha="center", bbox=label_box)
    ax.text(0.70, 0.685, "False", color=DARK, weight="bold", fontsize=10, ha="center", bbox=label_box)
    arrow(ax, (0.25, 0.296), (0.42, 0.224))
    arrow(ax, (0.75, 0.296), (0.58, 0.224))
    save(fig, "ch04_decision_trace")


def generate_loop_trace() -> None:
    fig, ax = blank_canvas(10.5, 5.1)
    ax.text(0.5, 0.95, "A loop trace records state after each iteration", ha="center", fontsize=16, weight="bold", color=DARK)
    columns = ["Iteration", "area", "total before", "total after"]
    rows = [["1", "18", "0", "18"], ["2", "24", "18", "42"], ["3", "15", "42", "57"]]
    table = ax.table(cellText=rows, colLabels=columns, cellLoc="center", bbox=[0.08, 0.29, 0.84, 0.48])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    for (row, _col), cell_obj in table.get_celld().items():
        cell_obj.set_edgecolor(MID)
        cell_obj.set_facecolor("#E8F2FC" if row == 0 else "white")
        if row == 0:
            cell_obj.set_text_props(weight="bold", color=DARK)
    ax.text(0.5, 0.18, "for area in [18, 24, 15]:    total = total + area", ha="center", family="monospace", color=DARK)
    ax.text(0.5, 0.08, "Invariant: total equals the sum of every area processed so far.", ha="center", color="#52647C")
    save(fig, "ch05_loop_trace")


def generate_call_stack() -> None:
    fig, ax = blank_canvas(10.5, 5.0)
    ax.text(0.5, 0.95, "Function calls create temporary stack frames", ha="center", fontsize=16, weight="bold", color=DARK)
    rounded_box(ax, (0.28, 0.13), 0.44, 0.17, "module frame", subtitle="rooms, report")
    rounded_box(ax, (0.28, 0.36), 0.44, 0.17, "report(room) frame", subtitle="room, area")
    rounded_box(ax, (0.28, 0.59), 0.44, 0.17, "calculate_area(w, d) frame", subtitle="w=6, d=8, result=48")
    arrow(ax, (0.77, 0.23), (0.77, 0.67))
    ax.text(0.81, 0.45, "calls push\nframes upward", va="center", color=DARK, weight="bold")
    arrow(ax, (0.21, 0.67), (0.21, 0.23), linestyle="--")
    ax.text(0.17, 0.45, "returns pop\nframes downward", va="center", ha="right", color=DARK, weight="bold")
    ax.text(0.5, 0.05, "Local names disappear when a frame returns; the returned value can enter the caller's frame.", ha="center", color="#52647C")
    save(fig, "ch06_call_stack")


def generate_exception_flow() -> None:
    fig, ax = blank_canvas(11, 5.0)
    ax.text(0.5, 0.95, "try, except, else, and finally describe four roles", ha="center", fontsize=16, weight="bold", color=DARK)
    rounded_box(ax, (0.37, 0.70), 0.26, 0.15, "try", subtitle="run the risky operation")
    rounded_box(ax, (0.07, 0.37), 0.28, 0.17, "except ValueError", subtitle="handle this expected failure")
    rounded_box(ax, (0.65, 0.37), 0.28, 0.17, "else", subtitle="run only after success")
    rounded_box(ax, (0.37, 0.08), 0.26, 0.16, "finally", subtitle="run on either path")
    arrow(ax, (0.42, 0.686), (0.24, 0.554))
    arrow(ax, (0.58, 0.686), (0.76, 0.554), linestyle="--")
    label_box = dict(facecolor="white", edgecolor="none", pad=1.5)
    ax.text(0.18, 0.66, "matching error", color=DARK, fontsize=9, weight="bold", bbox=label_box)
    ax.text(0.82, 0.66, "no error", color=DARK, fontsize=9, weight="bold", bbox=label_box)
    arrow(ax, (0.24, 0.356), (0.42, 0.254))
    arrow(ax, (0.76, 0.356), (0.58, 0.254))
    save(fig, "ch08_exception_flow")


def generate_path_tree() -> None:
    fig, ax = blank_canvas(10.5, 5.2)
    ax.text(0.5, 0.95, "A relative path is interpreted from a working folder", ha="center", fontsize=16, weight="bold", color=DARK)
    nodes = [
        (0.545, 0.70, 0.25, "project/"),
        (0.39, 0.50, 0.25, "data/"),
        (0.70, 0.50, 0.25, "scripts/"),
        (0.39, 0.24, 0.25, "rooms.csv"),
        (0.70, 0.24, 0.25, "analyze.py"),
    ]
    for x, y, w, label in nodes:
        rounded_box(ax, (x, y), w, 0.14, label)
    arrow(ax, (0.60, 0.686), (0.515, 0.654))
    arrow(ax, (0.74, 0.686), (0.825, 0.654))
    arrow(ax, (0.515, 0.50), (0.515, 0.38))
    arrow(ax, (0.825, 0.50), (0.825, 0.38))
    ax.text(0.5, 0.10, 'From project/: Path("data") / "rooms.csv"', ha="center", family="monospace", color=DARK)
    save(fig, "ch10_path_tree")


def generate_vectorization_trace() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4), layout="constrained")
    fig.suptitle("A loop and a vectorized expression can describe the same transformation", fontsize=15, weight="bold", color=DARK)
    for ax in axes:
        ax.axis("off")
    axes[0].set_title("Element-by-element loop", weight="bold", color=DARK)
    axes[0].text(0.08, 0.76, "results = []\nfor value in values:\n    results.append(value * 1.1)", family="monospace", fontsize=11, va="top")
    axes[0].text(0.08, 0.25, "Python coordinates each iteration.", color="#52647C")
    axes[1].set_title("NumPy vectorized expression", weight="bold", color=DARK)
    axes[1].text(0.08, 0.76, "results = values * 1.1", family="monospace", fontsize=11, va="top")
    axes[1].text(0.08, 0.56, "[10, 20, 30]  ->  [11, 22, 33]", family="monospace", color=BLUE)
    axes[1].text(0.08, 0.25, "The array operation states the transformation directly.", color="#52647C")
    save(fig, "ch11_vectorization_trace")


def generate_dataframe_before_after() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.5), layout="constrained")
    fig.suptitle("A transformation should make its data change inspectable", fontsize=15, weight="bold", color=DARK)
    before = [["A", "18", "1"], ["B", "", "1"], ["C", "31", "2"], ["D", "24", "2"]]
    after = [["1", "1", "18"], ["2", "2", "55"]]
    specs = [
        (axes[0], before, ["room", "area_m2", "floor"], "Raw room table"),
        (axes[1], after, ["floor", "room_count", "total_area_m2"], "Grouped summary"),
    ]
    for ax, data, labels, title in specs:
        ax.axis("off")
        ax.set_title(title, color=DARK, weight="bold")
        table = ax.table(cellText=data, colLabels=labels, cellLoc="center", bbox=[0.03, 0.20, 0.94, 0.62])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        for (row, _col), cell_obj in table.get_celld().items():
            cell_obj.set_edgecolor(MID)
            cell_obj.set_facecolor("#E8F2FC" if row == 0 else "white")
            if row == 0:
                cell_obj.set_text_props(weight="bold", color=DARK)
    fig.text(0.5, 0.05, "clean -> group by floor -> aggregate count and sum", ha="center", family="monospace", color="#52647C")
    save(fig, "ch12_dataframe_before_after")


def chart_finish(ax):
    ax.spines[["top", "right"]].set_visible(False)


def generate_result_plots() -> None:
    days = [1, 2, 3, 4, 5]
    temperatures_c = [19.0, 20.5, 22.0, 21.0, 23.5]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.plot(days, temperatures_c, color="tab:blue", marker="o")
    ax.set_title("Indoor temperature over five days")
    ax.set_xlabel("Day")
    ax.set_ylabel("Temperature (degrees C)")
    ax.grid(axis="y", alpha=0.25)
    chart_finish(ax)
    save(fig, "c13_labeled_line")

    hours = [8, 10, 12, 14, 16, 18]
    daylight_percent = [18, 35, 52, 61, 43, 20]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.plot(hours, daylight_percent, color="tab:blue", marker="o", linewidth=2, label="Measured")
    ax.set(title="Daylight through the day", xlabel="Hour", ylabel="Daylight level (percent)")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    chart_finish(ax)
    save(fig, "c13_line_plot")

    north_c = [19.0, 20.0, 21.0, 21.5, 21.0, 20.0]
    south_c = [19.5, 21.0, 23.0, 24.0, 22.5, 21.0]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.plot(hours, north_c, color="tab:blue", marker="o", linestyle="-", label="North room")
    ax.plot(hours, south_c, color="tab:orange", marker="s", linestyle="--", label="South room")
    ax.set(title="Room temperature comparison", xlabel="Hour", ylabel="Temperature (degrees C)")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    chart_finish(ax)
    save(fig, "c13_two_lines")

    room_names = ["Lobby", "Office", "Cafe", "Studio"]
    areas_m2 = [24.0, 18.0, 31.0, 26.0]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    bars = ax.bar(room_names, areas_m2, color="tab:blue")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.set(title="Area by room", xlabel="Room", ylabel="Area (m2)")
    ax.set_ylim(0, 36)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    chart_finish(ax)
    save(fig, "c13_bar_chart")

    materials = ["Reinforced concrete", "Cross-laminated timber", "Structural steel"]
    quantities_m3 = [42.0, 28.0, 16.0]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.barh(materials, quantities_m3, color="tab:orange")
    ax.set(title="Material quantities", xlabel="Quantity (m3)", ylabel="Material")
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)
    chart_finish(ax)
    save(fig, "c13_horizontal_bar")

    window_percent = [18, 22, 28, 35, 41, 48, 55]
    daylight_percent = [24, 29, 37, 45, 53, 58, 66]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.scatter(window_percent, daylight_percent, color="tab:blue", edgecolor="black", alpha=0.8)
    ax.set(title="Window area and daylight", xlabel="Window area (percent of wall)", ylabel="Daylight level (percent)")
    ax.grid(alpha=0.2)
    chart_finish(ax)
    save(fig, "c13_scatter_plot")

    room_areas_m2 = [15, 18, 18, 20, 21, 22, 22, 23, 24, 24, 25, 26, 27, 28, 30, 31, 33, 35, 38, 42]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.hist(room_areas_m2, bins=[10, 20, 30, 40, 50], color="tab:blue", edgecolor="black")
    ax.set(title="Distribution of room areas", xlabel="Area (m2)", ylabel="Number of rooms")
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    chart_finish(ax)
    save(fig, "c13_histogram")

    rooms = pd.DataFrame({"room": room_names, "area_m2": areas_m2})
    ordered = rooms.sort_values("area_m2")
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.barh(ordered["room"], ordered["area_m2"], color="tab:blue")
    ax.set(title="Room areas from a DataFrame", xlabel="Area (m2)", ylabel="Room")
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)
    chart_finish(ax)
    save(fig, "c13_dataframe_plot")

    data = pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "energy_kwh": [820, 760, 690, 610, 540, 500],
            "temperature_c": [2, 4, 8, 13, 18, 22],
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4), layout="constrained")
    axes[0].plot(data["month"], data["energy_kwh"], color="tab:blue", marker="o")
    axes[0].set(title="Monthly energy", xlabel="Month", ylabel="Energy (kWh)")
    axes[1].scatter(data["temperature_c"], data["energy_kwh"], color="tab:orange", marker="s", edgecolor="black")
    axes[1].set(title="Energy and temperature", xlabel="Outdoor temperature (degrees C)", ylabel="Energy (kWh)")
    for axis in axes:
        axis.grid(alpha=0.2)
        chart_finish(axis)
    save(fig, "c13_two_subplots")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    energy_kwh = [820, 760, 690, 610, 540, 500]
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.plot(months, energy_kwh, color="tab:blue", marker="o")
    ax.annotate("Lowest value", xy=("Jun", 500), xytext=("Apr", 700), arrowprops={"arrowstyle": "->", "color": "black"})
    ax.set(title="Monthly energy use", xlabel="Month", ylabel="Energy (kWh)")
    ax.grid(axis="y", alpha=0.25)
    chart_finish(ax)
    save(fig, "c13_annotation")


def generate_visualization_showcase() -> None:
    """Create a compact gallery inspired by the course-description showcase."""
    rng = np.random.default_rng(7)
    fig = plt.figure(figsize=(11, 7.2), layout="constrained")
    axes = [fig.add_subplot(2, 3, index + 1) for index in range(5)]
    surface_ax = fig.add_subplot(2, 3, 6, projection="3d")
    fig.suptitle("Visualization showcase: choose the view that answers the question", fontsize=16, weight="bold", color=DARK)

    months = np.arange(1, 13)
    energy = np.array([82, 78, 71, 62, 55, 49, 47, 50, 58, 67, 76, 84])
    uncertainty = np.array([6, 6, 5, 5, 4, 4, 4, 4, 5, 5, 6, 6])
    axes[0].plot(months, energy, color="tab:blue", marker="o", linewidth=1.8)
    axes[0].fill_between(months, energy - uncertainty, energy + uncertainty, color="tab:blue", alpha=0.18)
    axes[0].set(title="Trend + uncertainty", xlabel="Month", ylabel="Energy index")

    occupancy = np.array(
        [
            [5, 8, 22, 45, 68, 72],
            [4, 7, 25, 52, 75, 78],
            [3, 6, 28, 58, 80, 76],
            [3, 6, 24, 50, 73, 70],
        ]
    )
    image = axes[1].imshow(occupancy, cmap="Blues", aspect="auto", vmin=0, vmax=100)
    axes[1].set(title="Annotated heatmap", xlabel="Time block", ylabel="Zone")
    for row in range(occupancy.shape[0]):
        for col in range(occupancy.shape[1]):
            axes[1].text(col, row, occupancy[row, col], ha="center", va="center", fontsize=7, color="black")
    fig.colorbar(image, ax=axes[1], shrink=0.72, label="Occupancy (%)")

    distributions = [rng.normal(20, 2.3, 60), rng.normal(23, 3.5, 60), rng.normal(18, 1.5, 60)]
    violin = axes[2].violinplot(distributions, showmedians=True)
    for body in violin["bodies"]:
        body.set_facecolor(BLUE)
        body.set_alpha(0.45)
    axes[2].set(title="Distribution shapes", xlabel="Room type", ylabel="Temperature (C)", xticks=[1, 2, 3], xticklabels=["Studio", "Hall", "Office"])

    floors = np.arange(1, 7)
    office = np.array([0, 0, 420, 440, 430, 410])
    studio = np.array([220, 240, 180, 160, 150, 140])
    support = np.array([110, 115, 120, 120, 125, 120])
    axes[3].stackplot(floors, office, studio, support, labels=["Office", "Studio", "Support"], colors=[BLUE, ORANGE, "#8A8A8A"], alpha=0.85)
    axes[3].set(title="Composition by floor", xlabel="Floor", ylabel="Area (m2)")
    axes[3].legend(fontsize=7, loc="upper left")

    x = np.linspace(0, 1, 80)
    y = np.linspace(0, 1, 80)
    xx, yy = np.meshgrid(x, y)
    objective = (xx - 0.72) ** 2 + 1.8 * (yy - 0.38) ** 2 + 0.08 * np.sin(10 * xx) * np.cos(8 * yy)
    contour = axes[4].contourf(xx, yy, objective, levels=14, cmap="YlGnBu_r")
    axes[4].plot(0.72, 0.38, marker="*", markersize=11, color="tab:red")
    axes[4].set(title="Optimization landscape", xlabel="Window ratio", ylabel="Insulation level")
    fig.colorbar(contour, ax=axes[4], shrink=0.72, label="Objective")

    sx = np.linspace(-2.5, 2.5, 60)
    sy = np.linspace(-2.5, 2.5, 60)
    sxx, syy = np.meshgrid(sx, sy)
    radius = np.sqrt(sxx**2 + syy**2)
    szz = np.cos(radius * 2.3) * np.exp(-0.18 * radius**2)
    surface_ax.plot_surface(sxx, syy, szz, cmap="viridis", linewidth=0, antialiased=True)
    surface_ax.set(title="3D response surface", xlabel="x", ylabel="y", zlabel="response")
    surface_ax.view_init(elev=27, azim=-55)

    for axis in axes:
        axis.grid(alpha=0.18)
        chart_finish(axis)
    save(fig, "c13_visualization_showcase")


def generate_building_dashboard() -> None:
    """Create the rendered result for the longer building-dashboard script."""
    rng = np.random.default_rng(12)
    months = np.arange(1, 13)
    heating = np.array([52, 46, 35, 22, 12, 5, 3, 4, 10, 24, 38, 49])
    cooling = np.array([2, 3, 5, 9, 18, 31, 38, 36, 24, 12, 5, 2])
    lighting = np.array([18, 17, 16, 15, 14, 13, 13, 13, 14, 15, 17, 18])
    equipment = np.full(12, 21)
    outdoor_c = np.array([-2, 0, 5, 11, 17, 22, 25, 24, 20, 13, 7, 1])
    occupancy = np.clip(rng.normal(38, 22, size=(7, 24)), 0, 100)
    occupancy[:, :7] *= 0.15
    occupancy[:, 19:] *= 0.25
    occupancy[5:, :] *= 0.35

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.2), layout="constrained")
    fig.suptitle("Building performance dashboard", fontsize=16, weight="bold", color=DARK)
    axes[0, 0].stackplot(months, heating, cooling, lighting, equipment, labels=["Heating", "Cooling", "Lighting", "Equipment"], colors=[BLUE, ORANGE, "#8A8A8A", "#C6A15B"], alpha=0.88)
    axes[0, 0].set(title="Monthly energy by end use", xlabel="Month", ylabel="Energy (MWh)")
    axes[0, 0].legend(fontsize=7, ncol=2, loc="upper center")
    axes[0, 1].plot(months, outdoor_c, color="tab:blue", marker="o")
    axes[0, 1].axhspan(18, 24, color="tab:green", alpha=0.14, label="Comfort reference")
    axes[0, 1].set(title="Outdoor temperature context", xlabel="Month", ylabel="Temperature (C)")
    axes[0, 1].legend(fontsize=7)
    heatmap = axes[1, 0].imshow(occupancy, cmap="YlOrRd", aspect="auto", vmin=0, vmax=100)
    axes[1, 0].set(title="Weekly occupancy pattern", xlabel="Hour", ylabel="Day", yticks=range(7), yticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    fig.colorbar(
        heatmap,
        ax=axes[1, 0],
        orientation="horizontal",
        fraction=0.08,
        pad=0.14,
        label="Occupancy (%)",
    )
    totals = heating + cooling + lighting + equipment
    axes[1, 1].bar(months, totals, color=BLUE)
    axes[1, 1].axhline(totals.mean(), color=ORANGE, linestyle="--", label=f"Mean {totals.mean():.1f}")
    axes[1, 1].set(title="Total monthly energy", xlabel="Month", ylabel="Energy (MWh)")
    axes[1, 1].legend(fontsize=7)
    for axis in axes.flat:
        axis.grid(alpha=0.18)
        chart_finish(axis)
    save(fig, "c13_building_dashboard")


def generate_data_spectrum() -> None:
    fig, ax = blank_canvas(11, 4.9)
    ax.text(0.5, 0.95, "Structure is a spectrum, and it decides who does the work",
            ha="center", fontsize=15, weight="bold", color=DARK)

    classes = [
        ("Structured", "the file carries the schema",
         "BMS sensor logs, meter\nreadings, CSV exports",
         "Work: validate types,\nhandle missing values"),
        ("Semi-structured", "the file describes itself,\nbut irregularly",
         "JSON, XML, IFC/BIM,\nGeoJSON",
         "Work: flatten nested\nrecords into a table"),
        ("Unstructured", "nothing carries a schema\nfor the payload",
         "work orders, photos,\npoint clouds, PDFs",
         "Work: extract features\nyou choose and define"),
    ]
    xs = [0.03, 0.36, 0.69]
    for x, (title, carrier, examples, work) in zip(xs, classes):
        rounded_box(ax, (x, 0.44), 0.28, 0.30, title, subtitle=carrier)
        ax.text(x + 0.14, 0.35, examples, ha="center", va="top", fontsize=8.5, color="#52647C")
        ax.text(x + 0.14, 0.17, work, ha="center", va="top", fontsize=8.5,
                color=DARK, weight="bold")

    ax.annotate("", xy=(0.97, 0.83), xytext=(0.03, 0.83),
                arrowprops=dict(arrowstyle="-|>", linewidth=1.4, color=INK))
    ax.text(0.5, 0.865, "more of the structuring work falls on you",
            ha="center", fontsize=9, weight="bold", color=DARK)
    ax.text(0.5, 0.045,
            '"Unstructured" does not mean without structure. It means the structure is not in the file, so you must impose it.',
            ha="center", fontsize=9.5, color="#52647C")
    save(fig, "ch14_data_spectrum")


def generate_handling_paths() -> None:
    fig, ax = blank_canvas(11, 5.2)
    ax.text(0.5, 0.96, "Three kinds of source, three kinds of work, one destination",
            ha="center", fontsize=15, weight="bold", color=DARK)

    sources = [
        (0.76, "Structured", "sensor log CSV"),
        (0.50, "Semi-structured", "asset record JSON"),
        (0.24, "Unstructured", "work orders, photos"),
    ]
    operations = [
        (0.76, "Validate", "check dtypes,\nfill or drop gaps"),
        (0.50, "Flatten", "json_normalize,\nexplode records"),
        (0.24, "Extract features", "keyword flags,\nimage descriptors"),
    ]
    for (y, title, subtitle), (_, op_title, op_subtitle) in zip(sources, operations):
        rounded_box(ax, (0.02, y - 0.085), 0.24, 0.17, title, fontsize=10,
                    subtitle=subtitle)
        rounded_box(ax, (0.34, y - 0.085), 0.24, 0.17, op_title, fontsize=10,
                    subtitle=op_subtitle)
        arrow(ax, (0.265, y), (0.335, y))
        arrow(ax, (0.59, y), (0.685, 0.50))

    rounded_box(ax, (0.70, 0.385), 0.28, 0.23, "One feature table",
                subtitle="rows = samples\ncolumns = features", fill=True)
    ax.text(0.84, 0.31, "the X matrix that Chapters 19 to 22 require",
            ha="center", fontsize=8.5, color=DARK, weight="bold")
    ax.text(0.5, 0.04,
            "Every path ends in the same shape. What differs is how much work it takes to get there.",
            ha="center", fontsize=9.5, color="#52647C")
    save(fig, "ch14_handling_paths")


def generate_json_flatten() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), layout="constrained")
    fig.suptitle("Flattening turns a nested record into rows and columns",
                 fontsize=15, weight="bold", color=DARK)
    for ax in axes:
        ax.axis("off")

    axes[0].set_title("Nested JSON as stored", color=DARK, weight="bold")
    nested = (
        '{\n'
        '  "asset_id": "AHU-3",\n'
        '  "location": {\n'
        '    "building": "Link Hall",\n'
        '    "floor": 2\n'
        '  },\n'
        '  "filters": [\n'
        '    {"stage": 1, "type": "MERV8"},\n'
        '    {"stage": 2, "type": "MERV13"}\n'
        '  ]\n'
        '}'
    )
    axes[0].text(0.02, 0.93, nested, family="monospace", fontsize=9.5,
                 va="top", color=DARK)
    axes[0].text(0.02, 0.08, "One asset, two filters, two levels of nesting.",
                 fontsize=9, color="#52647C")

    axes[1].set_title("After json_normalize with record_path", color=DARK, weight="bold")
    rows = [["1", "MERV8", "AHU-3", "Link Hall"], ["2", "MERV13", "AHU-3", "Link Hall"]]
    table = axes[1].table(
        cellText=rows,
        colLabels=["stage", "type", "asset_id", "location.building"],
        cellLoc="center",
        bbox=[0.02, 0.45, 0.96, 0.36],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    for (row, _col), cell_obj in table.get_celld().items():
        cell_obj.set_edgecolor(MID)
        cell_obj.set_facecolor("#E8F2FC" if row == 0 else "white")
        if row == 0:
            cell_obj.set_text_props(weight="bold", color=DARK)
    axes[1].text(0.02, 0.30,
                 "record_path picks the repeating list;\n"
                 "meta carries the parent fields down to every row.",
                 fontsize=9, color="#52647C", va="top")
    save(fig, "ch14_json_flatten")


def generate_image_to_features() -> None:
    rng = np.random.default_rng(7)
    panel = np.zeros((48, 64, 3), dtype=np.int16)
    panel[:, :, 0], panel[:, :, 1], panel[:, :, 2] = 40, 60, 90
    rows_idx, cols_idx = np.ogrid[:48, :64]
    hot = ((rows_idx - 14) ** 2 + (cols_idx - 46) ** 2) < 90
    panel[hot] = [235, 175, 95]
    panel = np.clip(panel + rng.integers(-8, 9, panel.shape), 0, 255).astype(np.uint8)
    gray = panel.mean(axis=2)

    fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.2), layout="constrained")
    fig.suptitle("An image is already an array; a descriptor turns it into one table row",
                 fontsize=14.5, weight="bold", color=DARK)

    axes[0].imshow(panel)
    axes[0].set_title("Synthetic thermal panel", color=DARK, weight="bold", fontsize=11)
    axes[0].set_xlabel("width: 64 pixels")
    axes[0].set_ylabel("height: 48 pixels")
    axes[0].set_xticks([0, 32, 63])
    axes[0].set_yticks([0, 24, 47])

    axes[1].imshow(gray > 140, cmap="gray")
    axes[1].set_title("Pixels above the hot threshold", color=DARK, weight="bold", fontsize=11)
    axes[1].set_xlabel("9.28 percent of pixels")
    axes[1].set_xticks([])
    axes[1].set_yticks([])

    axes[2].axis("off")
    axes[2].set_title("One row of features", color=DARK, weight="bold", fontsize=11,
                      y=0.84)
    rows = [
        ["shape", "(48, 64, 3)"],
        ["mean_intensity", "73.06"],
        ["max_intensity", "175.00"],
        ["hot_fraction", "0.0928"],
    ]
    table = axes[2].table(cellText=rows, cellLoc="left", bbox=[0.02, 0.32, 0.96, 0.46])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (_row, col), cell_obj in table.get_celld().items():
        cell_obj.set_edgecolor(MID)
        cell_obj.set_facecolor("white")
        if col == 0:
            cell_obj.set_text_props(weight="bold", color=DARK)
    axes[2].text(0.02, 0.24,
                 "You choose these features.\nA different question would\nproduce a different row.",
                 fontsize=9, color="#52647C", va="top")
    save(fig, "ch14_image_to_features")


def generate_geodataframe_model() -> None:
    fig, ax = blank_canvas(10.8, 4.2)
    ax.text(0.5, 0.93, "A GeoDataFrame adds spatial meaning to a table", ha="center", fontsize=16, weight="bold", color=DARK)
    rounded_box(ax, (0.05, 0.38), 0.24, 0.30, "Attribute columns", subtitle="name, category, capacity")
    rounded_box(ax, (0.38, 0.38), 0.24, 0.30, "Geometry column", subtitle="Point, LineString, Polygon", fill=True)
    rounded_box(ax, (0.71, 0.38), 0.24, 0.30, "CRS", subtitle="how coordinates map to Earth")
    arrow(ax, (0.29, 0.53), (0.38, 0.53))
    arrow(ax, (0.62, 0.53), (0.71, 0.53))
    ax.text(0.5, 0.17, "The highlighted geometry column adds spatial methods; ordinary pandas operations still work on the rest of the table.", ha="center", color="#52647C")
    save(fig, "ch15_geodataframe_model")


def generate_site_buffer_map() -> None:
    import geopandas as gpd

    sites = pd.DataFrame(
        {
            "name": ["Main Hall", "Design Studio", "Transit Stop", "Library"],
            "longitude": [-76.1355, -76.1318, -76.1372, -76.1286],
            "latitude": [43.0386, 43.0371, 43.0410, 43.0395],
        }
    )
    points = gpd.GeoDataFrame(sites, geometry=gpd.points_from_xy(sites["longitude"], sites["latitude"]), crs="EPSG:4326").to_crs("EPSG:32618")
    service_areas = gpd.GeoDataFrame(points[["name"]].copy(), geometry=points.buffer(400), crs=points.crs)
    fig, ax = plt.subplots(figsize=(7.4, 5.2), layout="constrained")
    service_areas.plot(ax=ax, color="tab:blue", alpha=0.16, edgecolor="tab:blue", linewidth=1.2)
    points.plot(ax=ax, color="tab:orange", edgecolor="black", markersize=48, zorder=3)
    for row in points.itertuples():
        ax.annotate(row.name, (row.geometry.x, row.geometry.y), xytext=(5, 5), textcoords="offset points", fontsize=8)
    ax.set(title="Four 400 m site-service areas", xlabel="Easting (m), UTM zone 18N", ylabel="Northing (m), UTM zone 18N")
    ax.set_aspect("equal")
    ax.grid(alpha=0.18)
    chart_finish(ax)
    save(fig, "c15_site_buffers")


def generate_chicago_mapping_application() -> None:
    import geopandas as gpd
    import geodatasets

    chicago = gpd.read_file(geodatasets.get_path("geoda.chicago_commpop")).to_crs("EPSG:26916")
    groceries = gpd.read_file(geodatasets.get_path("geoda.groceries")).to_crs(chicago.crs)
    joined = gpd.sjoin(groceries, chicago[["community", "geometry"]], how="left", predicate="within")
    counts = joined.groupby("community").size().sort_values(ascending=False).head(10).sort_values()

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 5.4), layout="constrained")
    chicago.plot(column="POP2010", cmap="Blues", legend=True, edgecolor="white", linewidth=0.35, ax=axes[0], legend_kwds={"label": "Population in 2010", "shrink": 0.72})
    groceries.plot(ax=axes[0], color="tab:orange", edgecolor="black", linewidth=0.25, markersize=9, zorder=3)
    axes[0].set_title("Population and grocery locations")
    axes[0].set_axis_off()
    counts.plot.barh(ax=axes[1], color=BLUE)
    axes[1].set(title="Communities with the most mapped groceries", xlabel="Mapped grocery locations", ylabel="Community")
    axes[1].grid(axis="x", alpha=0.2)
    chart_finish(axes[1])
    fig.text(0.5, 0.01, "Source: GeoDa Center datasets distributed through geodatasets", ha="center", fontsize=8, color="#52647C")
    save(fig, "c16_chicago_mapping")


def generate_algorithm_growth() -> None:
    n = np.arange(1, 33)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8), layout="constrained")
    fig.suptitle("Input growth changes which algorithm remains practical", fontsize=15, weight="bold", color=DARK)
    axes[0].plot(n, np.ones_like(n), color="0.35", linestyle=":", label="constant: 1")
    axes[0].plot(n, np.log2(n), color=GREEN, linestyle="-.", label="logarithmic: log2(n)")
    axes[0].plot(n, n, color=BLUE, linestyle="-", label="linear: n")
    axes[0].plot(n, n**2, color=ORANGE, linestyle="--", label="quadratic: n squared")
    axes[0].set(xlabel="Input size n", ylabel="Approximate operations", title="Growth curves")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.2)
    chart_finish(axes[0])
    rows = [["10", "3", "10", "100"], ["100", "7", "100", "10,000"], ["1,000", "10", "1,000", "1,000,000"]]
    axes[1].axis("off")
    axes[1].set_title("Order-of-growth comparison", weight="bold", color=DARK)
    table = axes[1].table(cellText=rows, colLabels=["n", "log2(n)", "n", "n squared"], cellLoc="center", bbox=[0.02, 0.24, 0.96, 0.58])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (row, _col), cell_obj in table.get_celld().items():
        cell_obj.set_edgecolor(MID)
        cell_obj.set_facecolor("#E8F2FC" if row == 0 else "white")
        if row == 0:
            cell_obj.set_text_props(weight="bold", color=DARK)
    save(fig, "ch17_algorithm_growth")


def generate_binary_search_trace() -> None:
    values = [4, 9, 13, 18, 22, 27, 31, 36, 42]
    states = [(0, 8, 4), (5, 8, 6), (7, 8, 7)]
    fig, axes = plt.subplots(3, 1, figsize=(10.5, 5.8), layout="constrained")
    fig.suptitle("Binary search for 36 repeatedly discards half of a sorted range", fontsize=15, weight="bold", color=DARK)
    for step, (ax, (low, high, mid)) in enumerate(zip(axes, states), start=1):
        ax.set_xlim(-0.7, len(values) - 0.3)
        ax.set_ylim(0, 1)
        ax.axis("off")
        for index, value in enumerate(values):
            in_range = low <= index <= high
            face = "#E8F2FC" if in_range else "#F0F0F0"
            edge = ORANGE if index == mid else (BLUE if in_range else "#B8B8B8")
            ax.add_patch(Rectangle((index - 0.42, 0.27), 0.84, 0.46, facecolor=face, edgecolor=edge, linewidth=2 if index == mid else 1))
            ax.text(index, 0.53, str(value), ha="center", va="center", color=DARK, weight="bold" if index == mid else "normal")
            ax.text(index, 0.13, str(index), ha="center", va="center", color="#52647C", fontsize=8)
        relation = "too small" if values[mid] < 36 else "found"
        ax.text(-0.62, 0.53, f"Step {step}", ha="right", va="center", weight="bold", color=DARK)
        ax.text(len(values) - 0.35, 0.53, f"mid={mid}: {values[mid]} ({relation})", ha="left", va="center", color=ORANGE)
    save(fig, "ch17_binary_search_trace")


def generate_optimization_model() -> None:
    fig, ax = blank_canvas(11, 4.2)
    ax.text(0.5, 0.94, "An optimization model connects a decision to a verifiable recommendation", ha="center", fontsize=15, weight="bold", color=DARK)
    steps = [
        ("Variable", "window ratio r"),
        ("Objective", "energy + penalties"),
        ("Bounds", "0.10 <= r <= 0.70"),
        ("Search", "try candidate values"),
        ("Verified result", "best r and sensitivity"),
    ]
    xs = np.linspace(0.02, 0.81, len(steps))
    for x, (title, subtitle) in zip(xs, steps):
        rounded_box(ax, (x, 0.40), 0.15, 0.28, title, subtitle=subtitle)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, (left + 0.15, 0.54), (right, 0.54))
    ax.text(0.5, 0.15, "A solver optimizes the model you wrote; it cannot repair an unrealistic objective or missing constraint.", ha="center", color="#52647C")
    save(fig, "ch18_optimization_model")


def window_objective(ratio: float) -> float:
    energy = 80 + 160 * (ratio - 0.18) ** 2
    daylight_penalty = 450 * max(0.0, 0.32 - ratio) ** 2
    glare_penalty = 600 * max(0.0, ratio - 0.55) ** 2
    return energy + daylight_penalty + glare_penalty


def generate_optimization_application() -> None:
    from scipy.optimize import minimize_scalar

    ratios = np.linspace(0.10, 0.70, 241)
    energy = 80 + 160 * (ratios - 0.18) ** 2
    daylight = 450 * np.maximum(0.0, 0.32 - ratios) ** 2
    glare = 600 * np.maximum(0.0, ratios - 0.55) ** 2
    total = energy + daylight + glare
    result = minimize_scalar(window_objective, bounds=(0.10, 0.70), method="bounded")
    grid = np.linspace(0.10, 0.70, 13)
    fig, ax = plt.subplots(figsize=(8.4, 5.0), layout="constrained")
    ax.plot(ratios, energy, color="0.45", linestyle=":", label="Energy component")
    ax.plot(ratios, daylight + glare, color=ORANGE, linestyle="--", label="Daylight + glare penalties")
    ax.plot(ratios, total, color=BLUE, linewidth=2.2, label="Total objective")
    ax.scatter(grid, [window_objective(x) for x in grid], facecolors="white", edgecolors=DARK, label="Grid candidates", zorder=3)
    ax.scatter([result.x], [result.fun], color=ORANGE, edgecolor="black", marker="*", s=170, label=f"Bounded optimum: {result.x:.3f}", zorder=4)
    ax.set(title="Window-ratio optimization", xlabel="Window-to-wall ratio", ylabel="Objective value (lower is better)")
    ax.grid(alpha=0.2)
    ax.legend(fontsize=8)
    chart_finish(ax)
    save(fig, "ch18_window_optimization")


def generate_ml_workflow() -> None:
    fig, ax = blank_canvas(11, 4.3)
    ax.text(0.5, 0.94, "A defensible machine-learning workflow protects the final test", ha="center", fontsize=15, weight="bold", color=DARK)
    steps = [
        ("Define goal", "features X, target y"),
        ("Split once", "training and test data"),
        ("Fit on training", "learn parameters"),
        ("Predict test", "unseen examples"),
        ("Evaluate", "baseline + metrics"),
    ]
    xs = np.linspace(0.02, 0.81, len(steps))
    for x, (title, subtitle) in zip(xs, steps):
        rounded_box(ax, (x, 0.43), 0.15, 0.27, title, subtitle=subtitle)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, (left + 0.15, 0.565), (right, 0.565))
    ax.text(0.5, 0.18, "Do not use test outcomes to choose features, clean data, or tune the model; that leaks answers into evaluation.", ha="center", color="#52647C")
    save(fig, "ch19_ml_workflow")


def make_building_energy_data(seed: int = 42, sample_count: int = 240) -> tuple[pd.DataFrame, np.ndarray]:
    rng = np.random.default_rng(seed)
    data = pd.DataFrame(
        {
            "floor_area_m2": rng.uniform(80, 520, sample_count),
            "glazing_ratio": rng.uniform(0.12, 0.65, sample_count),
            "occupants": rng.integers(2, 45, sample_count),
            "outdoor_temp_c": rng.uniform(-5, 31, sample_count),
        }
    )
    noise = rng.normal(0, 10, sample_count)
    target = (
        28
        + 0.24 * data["floor_area_m2"]
        + 66 * data["glazing_ratio"]
        + 1.35 * data["occupants"]
        - 2.1 * data["outdoor_temp_c"]
        + noise
    ).to_numpy()
    return data, target


def generate_ml_diagnostics() -> None:
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.model_selection import train_test_split

    features, target = make_building_energy_data()
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.25, random_state=42)
    model = LinearRegression().fit(X_train, y_train)
    predictions = model.predict(X_test)
    residuals = y_test - predictions
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8), layout="constrained")
    axes[0].scatter(y_test, predictions, color=BLUE, edgecolor="black", alpha=0.76)
    limits = [min(y_test.min(), predictions.min()), max(y_test.max(), predictions.max())]
    axes[0].plot(limits, limits, color=ORANGE, linestyle="--", label="Perfect agreement")
    axes[0].set(title="Predicted versus actual test values", xlabel="Actual energy", ylabel="Predicted energy")
    axes[0].legend(fontsize=8)
    axes[1].scatter(predictions, residuals, color=BLUE, edgecolor="black", alpha=0.76)
    axes[1].axhline(0, color=ORANGE, linestyle="--")
    axes[1].set(title=f"Residual check (MAE={mae:.1f}, R2={r2:.2f})", xlabel="Predicted energy", ylabel="Actual - predicted")
    for ax in axes:
        ax.grid(alpha=0.2)
        chart_finish(ax)
    save(fig, "ch19_regression_diagnostics")


FACADE_BOUNDS = [(0.10, 0.70), (0.00, 1.20)]
FACADE_LOWS = np.array([low for low, _ in FACADE_BOUNDS])
FACADE_HIGHS = np.array([high for _, high in FACADE_BOUNDS])
FACADE_SPANS = FACADE_HIGHS - FACADE_LOWS


def facade_cost(decisions) -> float:
    """Smooth two-variable teaching objective; lower modeled cost is better."""
    window_ratio, shading_depth_m = decisions
    energy = (
        90
        + 180 * (window_ratio - 0.22) ** 2
        + 60 * (shading_depth_m - 0.45) ** 2
        - 70 * window_ratio * shading_depth_m
    )
    daylight_penalty = 500 * max(0.0, 0.25 - window_ratio) ** 2
    shading_cost = 40 * shading_depth_m**2
    return energy + daylight_penalty + shading_cost


def facade_gradient(decisions) -> np.ndarray:
    """Analytic partial derivatives of ``facade_cost``."""
    window_ratio, shading_depth_m = decisions
    d_ratio = (
        360 * (window_ratio - 0.22)
        - 70 * shading_depth_m
        - 1000 * max(0.0, 0.25 - window_ratio)
    )
    d_depth = 120 * (shading_depth_m - 0.45) - 70 * window_ratio + 80 * shading_depth_m
    return np.array([d_ratio, d_depth])


def rugged_facade_cost(decisions) -> float:
    """Add a manufacturing-increment ripple that creates many local minima."""
    window_ratio, shading_depth_m = decisions
    ripple = 6.0 * np.sin(12 * np.pi * window_ratio) * np.sin(8 * np.pi * shading_depth_m)
    return facade_cost(decisions) + ripple


def facade_surface(ratios: np.ndarray, depths: np.ndarray, rugged: bool = False) -> np.ndarray:
    """Vectorized objective used for contour plots."""
    smooth = (
        90
        + 180 * (ratios - 0.22) ** 2
        + 60 * (depths - 0.45) ** 2
        - 70 * ratios * depths
        + 500 * np.maximum(0.0, 0.25 - ratios) ** 2
        + 40 * depths**2
    )
    if not rugged:
        return smooth
    return smooth + 6.0 * np.sin(12 * np.pi * ratios) * np.sin(8 * np.pi * depths)


def projected_gradient_descent(cost, gradient_of, start, learning_rate,
                               iterations=400, tolerance=1e-6):
    """Fixed-step descent that clips every step back into the feasible box."""
    point = np.clip(np.array(start, dtype=float), FACADE_LOWS, FACADE_HIGHS)
    path = [point.copy()]
    values = [cost(point)]
    for _ in range(iterations):
        moved = np.clip(point - learning_rate * gradient_of(point), FACADE_LOWS, FACADE_HIGHS)
        path.append(moved.copy())
        values.append(cost(moved))
        step_size = np.linalg.norm(moved - point)
        point = moved
        if step_size < tolerance:
            break
    return point, np.array(path), np.array(values)


def facade_random_search(cost, seed=7, evaluations=4000):
    rng = np.random.default_rng(seed)
    best, best_cost, history = None, np.inf, []
    for _ in range(evaluations):
        candidate = FACADE_LOWS + rng.random(2) * FACADE_SPANS
        value = cost(candidate)
        if value < best_cost:
            best, best_cost = candidate, value
        history.append(best_cost)
    return best, best_cost, np.array(history)


def facade_annealing(cost, seed=7, evaluations=4000, start_temperature=20.0,
                     cooling=0.999, step_fraction=0.12):
    rng = np.random.default_rng(seed)
    current = FACADE_LOWS + rng.random(2) * FACADE_SPANS
    current_cost = cost(current)
    best, best_cost = current.copy(), current_cost
    history = [best_cost]
    temperature = start_temperature
    for _ in range(evaluations - 1):
        candidate = np.clip(
            current + rng.normal(0, step_fraction * FACADE_SPANS),
            FACADE_LOWS,
            FACADE_HIGHS,
        )
        candidate_cost = cost(candidate)
        change = candidate_cost - current_cost
        if change <= 0 or rng.random() < np.exp(-change / temperature):
            current, current_cost = candidate, candidate_cost
            if current_cost < best_cost:
                best, best_cost = current.copy(), current_cost
        temperature *= cooling
        history.append(best_cost)
    return best, best_cost, np.array(history)


def facade_genetic(cost, seed=7, population_size=40, generations=100,
                   mutation_probability=0.25, mutation_fraction=0.08, elite_count=2):
    rng = np.random.default_rng(seed)

    def tournament(population, scores):
        contenders = rng.choice(len(population), 3, replace=False)
        return population[contenders[scores[contenders].argmin()]]

    population = FACADE_LOWS + rng.random((population_size, 2)) * FACADE_SPANS
    scores = np.array([cost(row) for row in population])
    history = list(np.minimum.accumulate(scores))
    for _ in range(generations - 1):
        order = scores.argsort()
        population, scores = population[order], scores[order]
        children = [population[index].copy() for index in range(elite_count)]
        while len(children) < population_size:
            parent_a = tournament(population, scores)
            parent_b = tournament(population, scores)
            weight = rng.random()
            child = weight * parent_a + (1 - weight) * parent_b
            if rng.random() < mutation_probability:
                child = child + rng.normal(0, mutation_fraction * FACADE_SPANS)
            children.append(np.clip(child, FACADE_LOWS, FACADE_HIGHS))
        population = np.array(children)
        scores = np.array([cost(row) for row in population])
        history.extend(np.minimum(np.minimum.accumulate(scores), history[-1]))
    best_index = scores.argmin()
    return population[best_index], scores[best_index], np.array(history)


def facade_swarm(cost, seed=7, particle_count=30, iterations=134,
                 inertia=0.72, cognitive=1.5, social=1.5):
    rng = np.random.default_rng(seed)
    positions = FACADE_LOWS + rng.random((particle_count, 2)) * FACADE_SPANS
    velocities = rng.normal(0, 0.08, (particle_count, 2)) * FACADE_SPANS
    personal_best = positions.copy()
    personal_cost = np.array([cost(row) for row in positions])
    global_index = personal_cost.argmin()
    global_best = personal_best[global_index].copy()
    global_cost = personal_cost[global_index]
    history = list(np.minimum.accumulate(personal_cost))
    for _ in range(iterations - 1):
        toward_personal = rng.random((particle_count, 2))
        toward_global = rng.random((particle_count, 2))
        velocities = (
            inertia * velocities
            + cognitive * toward_personal * (personal_best - positions)
            + social * toward_global * (global_best - positions)
        )
        positions = np.clip(positions + velocities, FACADE_LOWS, FACADE_HIGHS)
        scores = np.array([cost(row) for row in positions])
        improved = scores < personal_cost
        personal_best[improved] = positions[improved]
        personal_cost[improved] = scores[improved]
        if personal_cost.min() < global_cost:
            global_index = personal_cost.argmin()
            global_best = personal_best[global_index].copy()
            global_cost = personal_cost[global_index]
        history.extend(np.minimum(np.minimum.accumulate(scores), history[-1]))
    return global_best, global_cost, np.array(history)


def generate_search_method_map() -> None:
    fig, ax = blank_canvas(11, 4.6)
    ax.text(
        0.5,
        0.95,
        "The landscape, not the language, decides which search method fits",
        ha="center",
        fontsize=15,
        weight="bold",
        color=DARK,
    )
    rounded_box(ax, (0.03, 0.52), 0.27, 0.30, "Smooth and single-valley",
                subtitle="use gradient descent or L-BFGS-B")
    rounded_box(ax, (0.36, 0.52), 0.27, 0.30, "Rugged or many valleys",
                subtitle="use a population or annealing search")
    rounded_box(ax, (0.69, 0.52), 0.28, 0.30, "Noisy or non-numeric",
                subtitle="use a derivative-free metaheuristic")
    rounded_box(ax, (0.03, 0.10), 0.27, 0.27, "Cheap gradient",
                subtitle="few evaluations, fast convergence")
    rounded_box(ax, (0.36, 0.10), 0.27, 0.27, "Many evaluations",
                subtitle="report budget and seed")
    rounded_box(ax, (0.69, 0.10), 0.28, 0.27, "Always benchmark",
                subtitle="random search is the honest baseline")
    for x in (0.165, 0.495, 0.83):
        arrow(ax, (x, 0.52), (x, 0.38))
    save(fig, "ch20_search_methods")


def generate_gradient_descent_figure() -> None:
    ratios = np.linspace(0.10, 0.70, 320)
    depths = np.linspace(0.00, 1.20, 320)
    mesh_ratio, mesh_depth = np.meshgrid(ratios, depths)
    surface = facade_surface(mesh_ratio, mesh_depth)

    start = [0.65, 0.60]
    _, path, _ = projected_gradient_descent(facade_cost, facade_gradient, start, 0.0025)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.9), layout="constrained")
    fig.suptitle(
        "Gradient descent follows the downhill direction of a smooth objective",
        fontsize=15,
        weight="bold",
        color=DARK,
    )
    contours = axes[0].contour(mesh_ratio, mesh_depth, surface, levels=18, colors="0.72", linewidths=0.8)
    axes[0].clabel(contours, inline=True, fontsize=6, fmt="%.0f")
    axes[0].plot(path[:, 0], path[:, 1], color=BLUE, marker="o", markersize=3.4,
                 linewidth=1.6, label="Descent path (rate 0.0025)")
    axes[0].scatter(*start, marker="X", s=110, color=ORANGE, edgecolor="black",
                    zorder=5, label="Start (0.65, 0.60)")
    axes[0].scatter(path[-1, 0], path[-1, 1], marker="*", s=190, color=GREEN,
                    edgecolor="black", zorder=5, label="Converged (0.292, 0.372)")
    axes[0].set(title="Search path on the cost contours",
                xlabel="Window-to-wall ratio", ylabel="Shading depth (m)")
    axes[0].legend(fontsize=7.5, loc="upper left")
    chart_finish(axes[0])

    styles = ((0.0005, "0.35", ":", "Rate 0.0005: stable but slow"),
              (0.0025, BLUE, "-", "Rate 0.0025: converges in 22 steps"),
              (0.0060, ORANGE, "--", "Rate 0.0060: overshoots and fails"))
    for rate, color, linestyle, label in styles:
        _, _, values = projected_gradient_descent(facade_cost, facade_gradient, start, rate)
        axes[1].plot(np.arange(len(values)), values, color=color, linestyle=linestyle,
                     linewidth=1.9, label=label)
    axes[1].axhline(89.23, color=GREEN, linewidth=1.2, linestyle="-.",
                    label="Best known cost 89.23")
    axes[1].set(title="The learning rate decides whether descent works",
                xlabel="Iteration", ylabel="Modeled cost (lower is better)",
                xlim=(0, 130), ylim=(85, 135))
    axes[1].grid(alpha=0.2)
    axes[1].legend(fontsize=7.5)
    chart_finish(axes[1])
    save(fig, "ch20_gradient_descent")


def generate_metaheuristic_comparison() -> None:
    ratios = np.linspace(0.10, 0.70, 420)
    depths = np.linspace(0.00, 1.20, 420)
    mesh_ratio, mesh_depth = np.meshgrid(ratios, depths)
    surface = facade_surface(mesh_ratio, mesh_depth, rugged=True)

    start = [0.65, 0.60]
    local_point, _, local_values = projected_gradient_descent(
        rugged_facade_cost,
        lambda candidate: np.array(
            [
                (
                    rugged_facade_cost(candidate + offset)
                    - rugged_facade_cost(candidate - offset)
                )
                / 2e-5
                for offset in (np.array([1e-5, 0.0]), np.array([0.0, 1e-5]))
            ]
        ),
        start,
        0.0025,
    )

    runs = (
        ("Random search", facade_random_search, "0.35", ":"),
        ("Simulated annealing", facade_annealing, ORANGE, "--"),
        ("Genetic algorithm", facade_genetic, BLUE, "-"),
        ("Particle swarm", facade_swarm, GREEN, "-."),
    )
    results = {name: runner(rugged_facade_cost) for name, runner, _, _ in runs}
    swarm_best = results["Particle swarm"][0]

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.9), layout="constrained")
    fig.suptitle(
        "On a rugged landscape a local method stops early while global searches keep exploring",
        fontsize=14,
        weight="bold",
        color=DARK,
    )
    filled = axes[0].contourf(mesh_ratio, mesh_depth, surface, levels=28, cmap="Blues_r", alpha=0.85)
    fig.colorbar(filled, ax=axes[0], label="Modeled cost")
    axes[0].scatter(*start, marker="X", s=110, color=ORANGE, edgecolor="black",
                    zorder=5, label="Start (0.65, 0.60)")
    axes[0].scatter(local_point[0], local_point[1], marker="s", s=90, color=ORANGE,
                    edgecolor="black", zorder=5,
                    label=f"Gradient descent stops: {local_values[-1]:.1f}")
    axes[0].scatter(swarm_best[0], swarm_best[1], marker="*", s=210, color=GREEN,
                    edgecolor="black", zorder=6,
                    label=f"Swarm best: {results['Particle swarm'][1]:.1f}")
    axes[0].set(title="Many local minima on the same feasible box",
                xlabel="Window-to-wall ratio", ylabel="Shading depth (m)")
    axes[0].legend(fontsize=7.5, loc="upper left")
    chart_finish(axes[0])

    for name, _, color, linestyle in runs:
        history = results[name][2]
        axes[1].plot(np.arange(1, len(history) + 1), history, color=color,
                     linestyle=linestyle, linewidth=1.8,
                     label=f"{name}: {results[name][1]:.2f}")
    axes[1].axhline(83.57, color="0.25", linewidth=1.1, linestyle=(0, (1, 3)),
                    label="Best known cost 83.57")
    axes[1].annotate(
        f"Gradient descent from the same start\nstops at {local_values[-1]:.2f}, above this panel",
        xy=(0.03, 0.93),
        xycoords="axes fraction",
        fontsize=8,
        color="#B03A2E",
        va="top",
    )
    axes[1].set(title="Best cost found per evaluation budget",
                xlabel="Objective evaluations (log scale)", ylabel="Best cost so far",
                xscale="log", ylim=(83.4, 92))
    axes[1].grid(alpha=0.2, which="both")
    axes[1].legend(fontsize=7.5, loc="upper right")
    chart_finish(axes[1])
    save(fig, "ch20_metaheuristic_search")


def make_comfort_complaint_data(seed: int = 42, sample_count: int = 900):
    """Reproducible synthetic comfort-complaint data with a non-linear driver."""
    rng = np.random.default_rng(seed)
    features = pd.DataFrame(
        {
            "floor_area_m2": rng.uniform(60, 520, sample_count),
            "glazing_ratio": rng.uniform(0.10, 0.68, sample_count),
            "occupant_density": rng.uniform(0.02, 0.16, sample_count),
            "setpoint_deviation_c": rng.normal(0.0, 2.4, sample_count),
            "outdoor_temp_c": rng.uniform(-8, 34, sample_count),
            "months_since_service": rng.integers(0, 36, sample_count),
        }
    )
    risk = (
        -9.0
        + 1.10 * np.abs(features["setpoint_deviation_c"])
        + 4.5 * features["glazing_ratio"] * (features["outdoor_temp_c"] > 26)
        + 30.0 * features["occupant_density"]
        + 0.11 * features["months_since_service"]
        + rng.normal(0, 0.30, sample_count)
    )
    probability = 1 / (1 + np.exp(-risk))
    target = pd.Series((rng.random(sample_count) < probability).astype(int), name="complaint")
    return features, target


def generate_classification_workflow() -> None:
    fig, ax = blank_canvas(11, 4.6)
    ax.text(
        0.5,
        0.95,
        "Model selection happens inside training data; the test set is opened once",
        ha="center",
        fontsize=14.5,
        weight="bold",
        color=DARK,
    )
    steps = [
        ("Split once", "stratified split"),
        ("Cross-validate", "compare on folds"),
        ("Tune", "search settings"),
        ("Refit", "refit best model"),
        ("Report once", "metrics, threshold"),
    ]
    xs = np.linspace(0.02, 0.81, len(steps))
    for x, (title, subtitle) in zip(xs, steps):
        rounded_box(ax, (x, 0.45), 0.15, 0.28, title, fontsize=10.5, subtitle=subtitle)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, (left + 0.15, 0.59), (right, 0.59))
    ax.text(0.5, 0.28, "Every comparison you make on the test set spends part of its independence.",
            ha="center", color="#52647C")
    ax.text(0.5, 0.14,
            "Accuracy alone hides the minority class: a majority-class rule scores 0.76 here and finds no complaint at all.",
            ha="center", color="#52647C", fontsize=9)
    save(fig, "ch21_classification_workflow")


def generate_model_selection_figure() -> None:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score, roc_curve
    from sklearn.model_selection import (
        StratifiedKFold,
        train_test_split,
        validation_curve,
    )
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier

    features, target = make_comfort_complaint_data()
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.25, random_state=42, stratify=target
    )
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    depths = np.arange(1, 16)
    train_scores, valid_scores = validation_curve(
        DecisionTreeClassifier(random_state=42),
        X_train,
        y_train,
        param_name="max_depth",
        param_range=depths,
        cv=folds,
        scoring="roc_auc",
    )

    logistic = Pipeline(
        [("scale", StandardScaler()), ("model", LogisticRegression(max_iter=1000))]
    ).fit(X_train, y_train)
    forest = RandomForestClassifier(
        n_estimators=400, max_depth=8, min_samples_leaf=5, random_state=42
    ).fit(X_train, y_train)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8), layout="constrained")
    fig.suptitle(
        "Validation curves expose overfitting; ROC curves compare ranking quality",
        fontsize=14.5,
        weight="bold",
        color=DARK,
    )
    axes[0].plot(depths, train_scores.mean(axis=1), color=ORANGE, linestyle="--",
                 marker="s", markersize=4, label="Training folds")
    axes[0].plot(depths, valid_scores.mean(axis=1), color=BLUE, linestyle="-",
                 marker="o", markersize=4, label="Validation folds")
    best_depth = depths[valid_scores.mean(axis=1).argmax()]
    axes[0].axvline(best_depth, color=GREEN, linestyle="-.", linewidth=1.3,
                    label=f"Best validated depth: {best_depth}")
    axes[0].set(title="Decision-tree depth versus cross-validated ROC-AUC",
                xlabel="Maximum tree depth", ylabel="ROC-AUC", ylim=(0.5, 1.02))
    axes[0].grid(alpha=0.2)
    axes[0].legend(fontsize=8, loc="lower left")
    chart_finish(axes[0])

    for name, model, color, linestyle in (
        ("Logistic regression", logistic, ORANGE, "--"),
        ("Tuned random forest", forest, BLUE, "-"),
    ):
        scores = model.predict_proba(X_test)[:, 1]
        false_rate, true_rate, _ = roc_curve(y_test, scores)
        axes[1].plot(false_rate, true_rate, color=color, linestyle=linestyle, linewidth=2.0,
                     label=f"{name}: AUC {roc_auc_score(y_test, scores):.3f}")
    axes[1].plot([0, 1], [0, 1], color="0.45", linestyle=":", linewidth=1.4,
                 label="Chance baseline: AUC 0.500")
    axes[1].set(title="Test-set ROC curves", xlabel="False positive rate",
                ylabel="True positive rate (recall)")
    axes[1].grid(alpha=0.2)
    axes[1].legend(fontsize=8, loc="lower right")
    chart_finish(axes[1])
    save(fig, "ch21_model_selection")


def generate_threshold_figure() -> None:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
    from sklearn.model_selection import train_test_split

    features, target = make_comfort_complaint_data()
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.25, random_state=42, stratify=target
    )
    forest = RandomForestClassifier(
        n_estimators=400, max_depth=8, min_samples_leaf=5, random_state=42
    ).fit(X_train, y_train)
    scores = forest.predict_proba(X_test)[:, 1]

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6), layout="constrained")
    fig.suptitle(
        "One fitted model produces many classifiers, one for each decision threshold",
        fontsize=14.5,
        weight="bold",
        color=DARK,
    )
    matrix = confusion_matrix(y_test, (scores >= 0.5).astype(int))
    axes[0].imshow(matrix, cmap="Blues", alpha=0.65)
    labels = (("True negative", "False positive"), ("False negative", "True positive"))
    for row in range(2):
        for column in range(2):
            axes[0].text(column, row - 0.12, str(matrix[row, column]), ha="center",
                         va="center", fontsize=17, weight="bold", color=DARK)
            axes[0].text(column, row + 0.18, labels[row][column], ha="center",
                         va="center", fontsize=8.5, color="#3B4A5F")
    axes[0].set(title="Confusion matrix at threshold 0.50",
                xlabel="Predicted label", ylabel="Actual label",
                xticks=[0, 1], yticks=[0, 1])
    axes[0].set_xticklabels(["No complaint", "Complaint"])
    axes[0].set_yticklabels(["No complaint", "Complaint"])

    thresholds = np.linspace(0.05, 0.95, 91)
    precision_line, recall_line, f1_line = [], [], []
    for threshold in thresholds:
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, (scores >= threshold).astype(int), average="binary", zero_division=0
        )
        precision_line.append(precision)
        recall_line.append(recall)
        f1_line.append(f1)
    axes[1].plot(thresholds, precision_line, color=ORANGE, linestyle="--", linewidth=2.0,
                 label="Precision: of flagged rooms, share correct")
    axes[1].plot(thresholds, recall_line, color=BLUE, linestyle="-", linewidth=2.0,
                 label="Recall: of real complaints, share found")
    axes[1].plot(thresholds, f1_line, color=GREEN, linestyle="-.", linewidth=1.8,
                 label="F1: harmonic mean of the two")
    best_threshold = thresholds[int(np.argmax(f1_line))]
    axes[1].axvline(best_threshold, color="0.35", linestyle=":", linewidth=1.4,
                    label=f"Best F1 near threshold {best_threshold:.2f}")
    axes[1].set(title="Precision and recall trade off as the threshold moves",
                xlabel="Decision threshold on predicted probability",
                ylabel="Score", ylim=(0, 1.42))
    axes[1].grid(alpha=0.2)
    axes[1].legend(fontsize=7.5, loc="upper center", ncol=2, framealpha=0.95)
    chart_finish(axes[1])
    save(fig, "ch21_threshold_tradeoff")


def sigmoid(values: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-values))


def initialize_network(input_count: int, hidden_count: int, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0, np.sqrt(1 / input_count), (input_count, hidden_count)),
        "b1": np.zeros(hidden_count),
        "W2": rng.normal(0, np.sqrt(1 / hidden_count), (hidden_count, 1)),
        "b2": np.zeros(1),
    }


def forward_pass(parameters: dict, features: np.ndarray):
    hidden_output = np.tanh(features @ parameters["W1"] + parameters["b1"])
    output = hidden_output @ parameters["W2"] + parameters["b2"]
    return hidden_output, sigmoid(output).ravel()


def cross_entropy(probabilities: np.ndarray, targets: np.ndarray) -> float:
    safe = np.clip(probabilities, 1e-12, 1 - 1e-12)
    return float(-np.mean(targets * np.log(safe) + (1 - targets) * np.log(1 - safe)))


def backward_pass(parameters, features, targets, hidden_output, probabilities) -> dict:
    sample_count = features.shape[0]
    output_delta = ((probabilities - targets) / sample_count).reshape(-1, 1)
    hidden_delta = (output_delta @ parameters["W2"].T) * (1 - hidden_output**2)
    return {
        "W1": features.T @ hidden_delta,
        "b1": hidden_delta.sum(axis=0),
        "W2": hidden_output.T @ output_delta,
        "b2": output_delta.sum(axis=0),
    }


def train_network(features, targets, hidden_count=8, learning_rate=0.5, epochs=400,
                  seed=0, validation_features=None, validation_targets=None):
    parameters = initialize_network(features.shape[1], hidden_count, seed)
    history = []
    for _ in range(epochs):
        hidden_output, probabilities = forward_pass(parameters, features)
        gradients = backward_pass(
            parameters, features, targets, hidden_output, probabilities
        )
        for key in parameters:
            parameters[key] -= learning_rate * gradients[key]
        row = [cross_entropy(probabilities, targets)]
        if validation_features is not None:
            row.append(
                cross_entropy(
                    forward_pass(parameters, validation_features)[1], validation_targets
                )
            )
        history.append(row)
    return parameters, np.array(history)


def generate_neuron_anatomy() -> None:
    fig, ax = blank_canvas(11, 4.6)
    ax.text(0.5, 0.95, "One neuron is a weighted sum followed by an activation",
            ha="center", fontsize=15, weight="bold", color=DARK)
    inputs = [
        ("setpoint deviation", 0.74),
        ("occupant density", 0.52),
        ("months since service", 0.30),
    ]
    for label, height in inputs:
        rounded_box(ax, (0.025, height - 0.055), 0.185, 0.11, label, fontsize=9)
    rounded_box(ax, (0.34, 0.40), 0.20, 0.24, "Weighted sum",
                subtitle="w1x1 + w2x2 + w3x3 + b")
    rounded_box(ax, (0.61, 0.40), 0.16, 0.24, "Activation",
                subtitle="tanh, ReLU, sigmoid", fill=True)
    rounded_box(ax, (0.84, 0.40), 0.14, 0.24, "Output", subtitle="to the next layer")
    for _, height in inputs:
        arrow(ax, (0.21, height), (0.325, 0.52))
    arrow(ax, (0.555, 0.52), (0.60, 0.52))
    arrow(ax, (0.785, 0.52), (0.83, 0.52))
    ax.text(0.27, 0.82, "each input carries\nits own weight", ha="center",
            fontsize=8.5, color="#52647C")
    ax.text(0.5, 0.16,
            "Without the activation the whole network collapses into a single weighted sum,",
            ha="center", color="#52647C")
    ax.text(0.5, 0.07,
            "so a stack of linear layers can express nothing that one linear layer cannot.",
            ha="center", color="#52647C")
    save(fig, "ch22_neuron_anatomy")


def generate_activation_functions() -> None:
    grid = np.linspace(-6, 6, 601)
    logistic = sigmoid(grid)
    hyperbolic = np.tanh(grid)
    rectified = np.maximum(0.0, grid)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5), layout="constrained")
    fig.suptitle(
        "An activation adds the curvature; its slope decides whether learning continues",
        fontsize=14.5, weight="bold", color=DARK,
    )
    for label, values, color, linestyle in (
        ("Sigmoid", logistic, ORANGE, "--"),
        ("Tanh", hyperbolic, BLUE, "-"),
        ("ReLU", rectified, GREEN, "-."),
    ):
        axes[0].plot(grid, values, color=color, linestyle=linestyle, linewidth=2.0, label=label)
    axes[0].axhline(0, color="0.7", linewidth=0.8)
    axes[0].axvline(0, color="0.7", linewidth=0.8)
    axes[0].set(title="Activation functions", xlabel="Weighted sum reaching the neuron",
                ylabel="Neuron output", ylim=(-1.4, 3.0))
    axes[0].grid(alpha=0.2)
    axes[0].legend(fontsize=8.5)
    chart_finish(axes[0])

    for label, values, color, linestyle in (
        ("Sigmoid slope", logistic * (1 - logistic), ORANGE, "--"),
        ("Tanh slope", 1 - hyperbolic**2, BLUE, "-"),
        ("ReLU slope", (grid > 0).astype(float), GREEN, "-."),
    ):
        axes[1].plot(grid, values, color=color, linestyle=linestyle, linewidth=2.0, label=label)
    axes[1].axvspan(-6, -3, color="0.85", alpha=0.5)
    axes[1].axvspan(3, 6, color="0.85", alpha=0.5)
    axes[1].text(-3.5, 0.62, "shaded: saturated region,\nslope near zero, learning stalls",
                 ha="center", fontsize=8.5, color="#52647C")
    axes[1].set(title="Slope of each activation", xlabel="Weighted sum reaching the neuron",
                ylabel="Derivative", ylim=(-0.05, 1.15))
    axes[1].grid(alpha=0.2)
    axes[1].legend(fontsize=8.5, loc="upper left")
    chart_finish(axes[1])
    save(fig, "ch22_activations")


def generate_network_training() -> None:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.neural_network import MLPClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    features, target = make_comfort_complaint_data()
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.25, random_state=42, stratify=target
    )
    scaler = StandardScaler().fit(X_train)
    scaled_train = scaler.transform(X_train)
    scaled_test = scaler.transform(X_test)
    _, history = train_network(
        scaled_train,
        y_train.to_numpy().astype(float),
        hidden_count=8,
        learning_rate=0.5,
        epochs=400,
        seed=0,
        validation_features=scaled_test,
        validation_targets=y_test.to_numpy().astype(float),
    )

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.7), layout="constrained")
    fig.suptitle(
        "Training drives the loss down; the hidden layer buys a curved decision boundary",
        fontsize=14.5, weight="bold", color=DARK,
    )
    epochs = np.arange(1, len(history) + 1)
    axes[0].plot(epochs, history[:, 0], color=BLUE, linestyle="-", linewidth=2.0,
                 label=f"Training loss: {history[-1, 0]:.3f}")
    axes[0].plot(epochs, history[:, 1], color=ORANGE, linestyle="--", linewidth=2.0,
                 label=f"Held-out loss: {history[-1, 1]:.3f}")
    axes[0].set(title="Binary cross-entropy during 400 full-batch epochs",
                xlabel="Epoch", ylabel="Mean cross-entropy loss")
    axes[0].grid(alpha=0.2)
    axes[0].legend(fontsize=8.5)
    chart_finish(axes[0])

    pair = ["setpoint_deviation_c", "occupant_density"]
    pair_train = X_train[pair]
    linear = Pipeline([
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000)),
    ]).fit(pair_train, y_train)
    network = Pipeline([
        ("scale", StandardScaler()),
        ("model", MLPClassifier(hidden_layer_sizes=(16,), alpha=1e-3,
                                max_iter=4000, random_state=42)),
    ]).fit(pair_train, y_train)

    deviation = np.linspace(-8, 8, 260)
    density = np.linspace(0.02, 0.16, 260)
    mesh_deviation, mesh_density = np.meshgrid(deviation, density)
    grid_frame = pd.DataFrame(
        {pair[0]: mesh_deviation.ravel(), pair[1]: mesh_density.ravel()}
    )
    surface = network.predict_proba(grid_frame)[:, 1].reshape(mesh_deviation.shape)
    linear_surface = linear.predict_proba(grid_frame)[:, 1].reshape(mesh_deviation.shape)

    filled = axes[1].contourf(mesh_deviation, mesh_density, surface, levels=20,
                              cmap="Blues", alpha=0.75)
    fig.colorbar(filled, ax=axes[1], label="Network complaint probability")
    axes[1].contour(mesh_deviation, mesh_density, surface, levels=[0.5],
                    colors=[BLUE], linewidths=2.2)
    axes[1].contour(mesh_deviation, mesh_density, linear_surface, levels=[0.5],
                    colors=[ORANGE], linewidths=2.2, linestyles="--")
    axes[1].scatter(pair_train[pair[0]][y_train == 0], pair_train[pair[1]][y_train == 0],
                    s=9, color="0.35", marker="o", alpha=0.55, label="No complaint")
    axes[1].scatter(pair_train[pair[0]][y_train == 1], pair_train[pair[1]][y_train == 1],
                    s=13, color=ORANGE, marker="^", edgecolor="black", linewidth=0.3,
                    alpha=0.9, label="Complaint")
    axes[1].plot([], [], color=BLUE, linewidth=2.2, label="Network boundary (0.50)")
    axes[1].plot([], [], color=ORANGE, linewidth=2.2, linestyle="--",
                 label="Logistic boundary (0.50)")
    axes[1].set(title="Two features, two decision boundaries",
                xlabel="Setpoint deviation (C)", ylabel="Occupant density")
    axes[1].legend(fontsize=7, loc="upper center", ncol=2, framealpha=0.92)
    chart_finish(axes[1])
    save(fig, "ch22_network_training")


def generate_network_capacity() -> None:
    from sklearn.model_selection import (
        StratifiedKFold,
        learning_curve,
        train_test_split,
        validation_curve,
    )
    from sklearn.neural_network import MLPClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    features, target = make_comfort_complaint_data()
    X_train, _, y_train, _ = train_test_split(
        features, target, test_size=0.25, random_state=42, stratify=target
    )
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    estimator = Pipeline([
        ("scale", StandardScaler()),
        ("model", MLPClassifier(alpha=1e-3, max_iter=2000, random_state=42)),
    ])

    widths = [(2,), (4,), (8,), (16,), (32,), (64,), (128,)]
    train_scores, valid_scores = validation_curve(
        estimator, X_train, y_train,
        param_name="model__hidden_layer_sizes", param_range=widths,
        cv=folds, scoring="roc_auc",
    )
    neuron_counts = [width[0] for width in widths]

    sizes, curve_train, curve_valid = learning_curve(
        Pipeline([
            ("scale", StandardScaler()),
            ("model", MLPClassifier(hidden_layer_sizes=(16,), alpha=1e-3,
                                    max_iter=2000, random_state=42)),
        ]),
        X_train, y_train, cv=folds, scoring="roc_auc",
        train_sizes=np.linspace(0.2, 1.0, 5),
    )

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.7), layout="constrained")
    fig.suptitle(
        "Width controls capacity; the learning curve says whether more rows would help",
        fontsize=14.5, weight="bold", color=DARK,
    )
    axes[0].plot(neuron_counts, train_scores.mean(axis=1), color=ORANGE, linestyle="--",
                 marker="s", markersize=5, label="Training folds")
    axes[0].plot(neuron_counts, valid_scores.mean(axis=1), color=BLUE, linestyle="-",
                 marker="o", markersize=5, label="Validation folds")
    axes[0].fill_between(
        neuron_counts,
        valid_scores.mean(axis=1) - valid_scores.std(axis=1),
        valid_scores.mean(axis=1) + valid_scores.std(axis=1),
        color=BLUE, alpha=0.13, label="Validation spread (1 s.d.)",
    )
    axes[0].set(title="Hidden-layer width versus cross-validated ROC-AUC",
                xlabel="Neurons in the hidden layer", ylabel="ROC-AUC",
                xscale="log", ylim=(0.68, 1.02))
    axes[0].set_xticks(neuron_counts)
    axes[0].set_xticklabels([str(count) for count in neuron_counts])
    axes[0].grid(alpha=0.2)
    axes[0].legend(fontsize=8, loc="upper left")
    chart_finish(axes[0])

    axes[1].plot(sizes, curve_train.mean(axis=1), color=ORANGE, linestyle="--",
                 marker="s", markersize=5, label="Training folds")
    axes[1].plot(sizes, curve_valid.mean(axis=1), color=BLUE, linestyle="-",
                 marker="o", markersize=5, label="Validation folds")
    axes[1].set(title="Training rows versus cross-validated ROC-AUC",
                xlabel="Training rows used", ylabel="ROC-AUC", ylim=(0.68, 1.02))
    axes[1].grid(alpha=0.2)
    axes[1].legend(fontsize=8, loc="lower right")
    chart_finish(axes[1])
    save(fig, "ch22_network_capacity")


def main() -> None:
    generate_workflow_diagram()
    generate_program_pipeline()
    generate_expression_trace()
    generate_decision_trace()
    generate_loop_trace()
    generate_function_anatomy()
    generate_call_stack()
    generate_builtin_toolbox()
    generate_traceback_anatomy()
    generate_exception_flow()
    generate_copying_models()
    generate_file_pipeline()
    generate_path_tree()
    generate_array_axes()
    generate_vectorization_trace()
    generate_dataframe_pipeline()
    generate_dataframe_before_after()
    generate_result_plots()
    generate_visualization_showcase()
    generate_building_dashboard()
    generate_data_spectrum()
    generate_handling_paths()
    generate_json_flatten()
    generate_image_to_features()
    generate_geodataframe_model()
    generate_site_buffer_map()
    generate_chicago_mapping_application()
    generate_algorithm_growth()
    generate_binary_search_trace()
    generate_optimization_model()
    generate_optimization_application()
    generate_ml_workflow()
    generate_ml_diagnostics()
    generate_search_method_map()
    generate_gradient_descent_figure()
    generate_metaheuristic_comparison()
    generate_classification_workflow()
    generate_model_selection_figure()
    generate_threshold_figure()
    generate_neuron_anatomy()
    generate_activation_functions()
    generate_network_training()
    generate_network_capacity()
    print(f"Generated teaching figures in {OUTPUT}")


if __name__ == "__main__":
    main()
