"""Compare linear and binary search while counting comparisons."""

from pathlib import Path

import matplotlib.pyplot as plt


def linear_search(values, target):
    """Return (index, comparisons) after scanning from left to right."""
    comparisons = 0
    for index, value in enumerate(values):
        comparisons += 1
        if value == target:
            return index, comparisons
    return -1, comparisons


def binary_search(sorted_values, target):
    """Return (index, comparisons) by repeatedly halving a sorted range."""
    low = 0
    high = len(sorted_values) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        candidate = sorted_values[mid]

        if candidate == target:
            return mid, comparisons
        if candidate < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


# 1. Verify both algorithms on one small, readable example.
room_ids = [104, 112, 119, 125, 131, 144, 152, 167, 181]
target_id = 167

linear_result = linear_search(room_ids, target_id)
binary_result = binary_search(room_ids, target_id)

print("Linear search (index, comparisons):", linear_result)
print("Binary search (index, comparisons):", binary_result)
assert linear_result[0] == binary_result[0]

# 2. Compare operation counts as input size grows.
sizes = [16, 32, 64, 128, 256, 512, 1024]
linear_counts = []
binary_counts = []

for size in sizes:
    values = list(range(size))
    target = values[-1]
    _, linear_count = linear_search(values, target)
    _, binary_count = binary_search(values, target)
    linear_counts.append(linear_count)
    binary_counts.append(binary_count)

# 3. Communicate the algorithmic difference with line style and markers.
fig, ax = plt.subplots(figsize=(7.4, 4.8), layout="constrained")
ax.plot(
    sizes,
    linear_counts,
    color="tab:blue",
    marker="o",
    label="Linear search",
)
ax.plot(
    sizes,
    binary_counts,
    color="tab:orange",
    marker="s",
    linestyle="--",
    label="Binary search",
)
ax.set(
    title="Search comparisons as the input grows",
    xlabel="Number of sorted values",
    ylabel="Comparisons for the final value",
)
ax.grid(alpha=0.2)
ax.legend()

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "search_algorithm_comparison.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)
