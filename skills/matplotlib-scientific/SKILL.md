# Matplotlib Scientific Figure Skill

Use when creating matplotlib plots, scientific figures, or data visualizations.
Triggers - matplotlib, plot, figure, 그래프, 플롯, 시각화, visualization, "그려줘", "plot 만들어", scatter, histogram, violin

## Mandatory Rules

1. **One plot per script** - standalone Python file
2. **ALL text uses FontProperties** - no raw matplotlib text
3. **No Unicode math** - use `$_{sub}$` / `$^{sup}$` / `$\mathregular{_2}$`
4. **No grids, no bold, no `tight_layout()`, no `plt.show()`**
5. **SVG only** at 300 DPI, save to `./output/`
6. **All data within xlim/ylim** with 5-10% padding
7. **`ax.set_position([0.2, 0.2, 0.666, 0.333])`** always per plot

## Setup (copy to every script)

```python
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
import numpy as np
import os

matplotlib.rcParams['mathtext.default'] = 'regular'

fs, fss, fsss, fsl = 12, 12, 8, 24
font_properties_label = fm.FontProperties(family='Arial', size=fs)
font_properties_tick = fm.FontProperties(family='Arial', size=fss)
font_properties_annotate = fm.FontProperties(family='Arial', size=fsss)
font_properties_legend = fm.FontProperties(family='Arial', size=fss)

colors = ['#77AEB3', '#E5885D', '#C7C4B5', '#A1C2DE', '#B4944B']
os.makedirs('./output', exist_ok=True)
```

## Helper Functions (include in every script)

```python
def apply_font_styling(ax):
    for tick in ax.get_xticklabels():
        tick.set_fontproperties(font_properties_tick)
    for tick in ax.get_yticklabels():
        tick.set_fontproperties(font_properties_tick)

def format_axis_labels(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel, fontproperties=font_properties_label)
    ax.set_ylabel(ylabel, fontproperties=font_properties_label)
    apply_font_styling(ax)

def plot_series_with_style(ax, x_data, y_data, color, label, series_index=0):
    zorder = 2 - 0.1 * series_index
    ax.plot(x_data, y_data, color=color, label=label, linewidth=1.5, zorder=zorder)
    ax.scatter(x_data, y_data, color=color, s=100, marker='o', linewidth=1.5, zorder=zorder)

def create_subplot_layout(nrows=1, ncols=1, figsize=(4, 4)):
    return plt.subplots(nrows, ncols, figsize=figsize)

def save_plot(filename, dpi=300):
    if not filename.startswith('plot'):
        filename = f'plot1_{filename}'
    if not filename.endswith('.svg'):
        filename = filename.replace('.png', '.svg').replace('.pdf', '.svg')
        if not filename.endswith('.svg'):
            filename += '.svg'
    plt.savefig(f'./output/{filename}', dpi=dpi, bbox_inches='tight', format='svg')
```

## Math Text Rules

| Wrong | Correct | Case |
|-------|---------|------|
| `CH₄` | `CH$_{4}$` | Chemical subscript |
| `x²` | `x$^{2}$` | Superscript |
| `O₂` | `O$\mathregular{_2}$` | mathregular subscript |
| `10⁻³` | `10$^{-3}$` | Negative exponent |

## Legend: always `frameon=False, prop=font_properties_legend`

## Scientific Notation (for values >1000 or <0.001)

```python
from matplotlib.ticker import FuncFormatter

def scientific_formatter(x, pos):
    if x == 0: return '0'
    exponent = int(np.floor(np.log10(abs(x))))
    coeff = x / 10**exponent
    if coeff == 1: return f'10$^{{{exponent}}}$'
    elif coeff == int(coeff): return f'{int(coeff)}x10$^{{{exponent}}}$'
    else: return f'{coeff:.1f}x10$^{{{exponent}}}$'

ax.yaxis.set_major_formatter(FuncFormatter(scientific_formatter))
```

## Filename: `{num}_plot{n}_{description}.svg` (num = 1~n)

## Checklist

- [ ] `rcParams['mathtext.default'] = 'regular'` set
- [ ] `ax.set_position([0.2, 0.2, 0.666, 0.333])` done
- [ ] All text uses font_properties_*
- [ ] No grid, no bold, no tight_layout, no plt.show()
- [ ] Legend frameon=False
- [ ] SVG 300 DPI in ./output/
- [ ] All data visible within limits (5-10% padding)
- [ ] Colors from palette in order
