#!/usr/bin/env python3
"""Generate Before/After matplotlib comparison plots."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

os.makedirs('./output', exist_ok=True)
np.random.seed(42)

# ── Skill setup ──
matplotlib.rcParams['mathtext.default'] = 'regular'
fs, fss, fsss = 12, 12, 8
font_properties_label = fm.FontProperties(family='Arial', size=fs)
font_properties_tick = fm.FontProperties(family='Arial', size=fss)
font_properties_legend = fm.FontProperties(family='Arial', size=fss)
font_properties_title = fm.FontProperties(family='Arial', size=14)
colors = ['#77AEB3', '#C7C4B5', '#E5885D', '#A1C2DE', '#B4944B']

def apply_font_styling(ax):
    for tick in ax.get_xticklabels():
        tick.set_fontproperties(font_properties_tick)
    for tick in ax.get_yticklabels():
        tick.set_fontproperties(font_properties_tick)

# ── Data ──
# Scatter: DFT vs ML predicted energy
x_scatter = np.linspace(-5, 2, 30) + np.random.normal(0, 0.3, 30)
y_scatter = x_scatter * 0.95 + np.random.normal(0, 0.25, 30)

# Bar: Model pass rates
models = ['GPT-4o', 'Claude\nOpus', 'Gemini\nPro', 'Llama\n3.1', 'Mistral\nLarge']
vanilla = [62, 58, 54, 38, 42]
skill = [88, 92, 78, 56, 64]

# Line: Training convergence
epochs = np.arange(1, 51)
loss_a = 2.5 * np.exp(-0.06 * epochs) + 0.12 + np.random.normal(0, 0.03, 50)
loss_b = 2.5 * np.exp(-0.09 * epochs) + 0.08 + np.random.normal(0, 0.02, 50)


# ════════════════════════════════════════
# BEFORE (default matplotlib)
# ════════════════════════════════════════

# 1. Scatter - Before
fig, ax = plt.subplots(figsize=(5, 5))
ax.scatter(x_scatter, y_scatter, c='blue', alpha=0.7)
ax.plot([-6, 3], [-6, 3], 'r--', label='y = x')
ax.set_xlabel('DFT Energy (eV/atom)')
ax.set_ylabel('ML Predicted Energy (eV/atom)')
ax.set_title('DFT vs ML Prediction', fontweight='bold')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig('./output/before_scatter.png', dpi=150)
plt.close()

# 2. Bar - Before
fig, ax = plt.subplots(figsize=(6, 4))
x_pos = np.arange(len(models))
ax.bar(x_pos - 0.2, vanilla, 0.35, label='Vanilla', color='steelblue')
ax.bar(x_pos + 0.2, skill, 0.35, label='+Skill', color='coral')
ax.set_xlabel('Model')
ax.set_ylabel('Pass Rate (%)')
ax.set_title('LLM Benchmark: Vanilla vs +Skill', fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(models)
ax.legend()
ax.grid(True, axis='y')
plt.tight_layout()
plt.savefig('./output/before_bar.png', dpi=150)
plt.close()

# 3. Line - Before
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(epochs, loss_a, 'b-o', label='Baseline', markersize=3)
ax.plot(epochs, loss_b, 'r-s', label='Proposed', markersize=3)
ax.set_xlabel('Epoch')
ax.set_ylabel('Validation Loss')
ax.set_title('Training Convergence', fontweight='bold')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig('./output/before_line.png', dpi=150)
plt.close()


# ════════════════════════════════════════
# AFTER (matplotlib-scientific skill)
# ════════════════════════════════════════

# 1. Scatter - After
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_position([0.2, 0.2, 0.666, 0.666])
ax.scatter(x_scatter, y_scatter, c=colors[0], s=40, edgecolors='white', linewidth=0.5, zorder=2)
ax.plot([-6, 3], [-6, 3], '--', color=colors[2], linewidth=1, label='y = x', zorder=1)
ax.set_xlabel('DFT Energy (eV/atom)', fontproperties=font_properties_label)
ax.set_ylabel('ML Predicted Energy (eV/atom)', fontproperties=font_properties_label)
apply_font_styling(ax)
ax.legend(frameon=False, prop=font_properties_legend)
ax.set_xlim(-6.5, 3.5)
ax.set_ylim(-6.5, 3.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('./output/after_scatter.png', dpi=150, bbox_inches='tight', format='png')
plt.close()

# 2. Bar - After
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_position([0.2, 0.2, 0.666, 0.333])
x_pos = np.arange(len(models))
ax.bar(x_pos - 0.2, vanilla, 0.35, label='Vanilla', color=colors[0], edgecolor='white', linewidth=0.5)
ax.bar(x_pos + 0.2, skill, 0.35, label='+Skill', color=colors[2], edgecolor='white', linewidth=0.5)
ax.set_xlabel('Model', fontproperties=font_properties_label)
ax.set_ylabel('Pass Rate (%)', fontproperties=font_properties_label)
ax.set_xticks(x_pos)
ax.set_xticklabels(models, fontproperties=font_properties_tick)
apply_font_styling(ax)
ax.legend(frameon=False, prop=font_properties_legend)
ax.set_ylim(0, 105)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('./output/after_bar.png', dpi=150, bbox_inches='tight', format='png')
plt.close()

# 3. Line - After
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_position([0.2, 0.2, 0.666, 0.333])
ax.plot(epochs, loss_a, color=colors[0], linewidth=1.5, label='Baseline', zorder=2)
ax.scatter(epochs[::5], loss_a[::5], color=colors[0], s=30, marker='o', zorder=3, edgecolors='white', linewidth=0.5)
ax.plot(epochs, loss_b, color=colors[2], linewidth=1.5, label='Proposed', zorder=2)
ax.scatter(epochs[::5], loss_b[::5], color=colors[2], s=30, marker='s', zorder=3, edgecolors='white', linewidth=0.5)
ax.set_xlabel('Epoch', fontproperties=font_properties_label)
ax.set_ylabel('Validation Loss', fontproperties=font_properties_label)
apply_font_styling(ax)
ax.legend(frameon=False, prop=font_properties_legend)
ax.set_xlim(0, 52)
ax.set_ylim(0, 2.8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('./output/after_line.png', dpi=150, bbox_inches='tight', format='png')
plt.close()

print("Done. 6 images generated in ./output/")
