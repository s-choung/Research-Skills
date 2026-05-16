"""
Build ASE Benchmark bar chart — horizontal grouped bars.
Run: conda run -n base python build_barplot.py
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.transforms as transforms
from matplotlib.patches import Patch
import numpy as np

# ── Data (top-to-bottom display order) ───────────────────────────
data = [
    ("Gemini", [
        ("Flash-Lite", 44, 58),
        ("Flash",      36, 58),
        ("Pro",        32, 76),
    ]),
    ("OpenAI", [
        ("GPT-5.4-mini", 82, 90),
        ("GPT-5.4",      90, 90),
        ("GPT-5.5",     100, 100),
    ]),
    ("Claude", [
        ("Haiku 4.5",  52, 80),
        ("Sonnet 4.6", 86, 94),
        ("Opus 4.7",   84, 100),
    ]),
]

# ── Colors (lighter = w/o Skill, darker = w/ Skill) ─────────────
palette = {
    "Gemini": ("#b3cde3", "#4682b4"),
    "OpenAI": ("#a8ddb5", "#2e8b57"),
    "Claude": ("#e5b8a0", "#c05a3c"),
}
provider_color = {
    "Gemini": "#4682b4",
    "OpenAI": "#2e8b57",
    "Claude": "#c05a3c",
}

# ── Build y positions (top = high y, bottom = low y) ─────────────
bar_h = 0.32
model_spacing = 1.0      # y distance between model group centers
provider_spacing = 1.8    # extra gap between provider sections

# Assign y positions going downward
all_entries = []
provider_ranges = []

y = 0
for pi, (prov, models) in enumerate(data):
    if pi > 0:
        y -= provider_spacing
    y_top = y
    for mi, (mname, van, sk) in enumerate(models):
        if mi > 0:
            y -= model_spacing
        all_entries.append((prov, mname, van, sk, y))
    y_bot = y
    provider_ranges.append((prov, y_top, y_bot))

# ── Figure ────────────────────────────────────────────────────────
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["font.size"] = 12

fig, ax = plt.subplots(figsize=(10.5, 7.8))
fig.patch.set_facecolor("#fafaf7")
ax.set_facecolor("#fafaf7")

yticks = []
ytick_labels = []

for prov, mname, van, sk, yc in all_entries:
    light, dark = palette[prov]

    # w/o Skill bar ON TOP (higher y = upper position)
    y_wo = yc + bar_h * 0.55
    y_w  = yc - bar_h * 0.55

    ax.barh(y_wo, van, height=bar_h, color=light, edgecolor="white", linewidth=0.5)
    ax.barh(y_w,  sk,  height=bar_h, color=dark,  edgecolor="white", linewidth=0.5)

    # Percentage labels
    ax.text(van + 1.2, y_wo, f"{van}%", va="center", ha="left",
            fontsize=9.5, color="#888")
    ax.text(sk + 1.2, y_w, f"{sk}%", va="center", ha="left",
            fontsize=9.5, color=dark, fontweight="bold")

    yticks.append(yc)
    ytick_labels.append(mname)

# Model name labels
ax.set_yticks(yticks)
ax.set_yticklabels(ytick_labels, fontsize=12.5)

# Provider labels — positioned above the first model in each group
for prov, y_top, y_bot in provider_ranges:
    # Place above the topmost model of the group
    y_label = y_top + 0.65
    ax.annotate(
        prov,
        xy=(0, y_label),
        xycoords=("axes fraction", "data"),
        xytext=(4, 0),
        textcoords="offset points",
        fontsize=13, fontweight="bold",
        fontstyle="italic",
        color=provider_color[prov],
        va="bottom", ha="left",
        annotation_clip=False,
    )

# x axis
ax.set_xlim(0, 113)
ax.set_xlabel("Pass Rate (%)", fontsize=12, labelpad=8)
ax.xaxis.set_major_locator(plt.MultipleLocator(20))

# Grid and spines
ax.grid(axis="x", alpha=0.2, linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(0.5)
ax.spines["bottom"].set_linewidth(0.5)
ax.tick_params(axis="y", length=0, pad=10)

# y limits with padding
y_min = min(e[4] for e in all_entries) - 0.9
y_max = max(e[4] for e in all_entries) + 1.4
ax.set_ylim(y_min, y_max)

# Legend
legend_elements = [
    Patch(facecolor="#b0b0b0", edgecolor="none", label="w/o Skill"),
    Patch(facecolor="#555555", edgecolor="none", label="w/ Skill"),
]
ax.legend(handles=legend_elements, loc="center",
          fontsize=11, frameon=True, fancybox=False,
          edgecolor="#ccc", facecolor="#fafaf7",
          bbox_to_anchor=(0.88, -0.10), ncol=2)

plt.tight_layout()
plt.subplots_adjust(left=0.25)

out = "/Users/sean/Research-Skills/assets/ase_bench_barplot.png"
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="#fafaf7")
print(f"Saved: {out}")
plt.close()
