"""Shared style for the round-2 figures (fig_r2_*.py).

Colour rule for the whole representation report:
  internal (16-ligand LOLO)      teal   #77AEB3
  external (46 new ligands)      orange #E5885D
Marker rule by model family:
  GP family (GP-Matern, GP-ARD)  circle
  table models (TabPFN, HistGB)  square
  linear (Ridge, KRR-RBF)        triangle
"""
import os

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

matplotlib.rcParams['mathtext.default'] = 'regular'
# Keep SVG text as <text> rather than glyph outlines. The report inlines about
# 110 figures, and the duplicated outlines cost roughly 2 MB of the page.
matplotlib.rcParams['svg.fonttype'] = 'none'
fs, fss, fsss, fsl = 18, 16, 16, 20
font_properties_label = fm.FontProperties(family='Arial', size=fs)
font_properties_tick = fm.FontProperties(family='Arial', size=fss)
font_properties_annotate = fm.FontProperties(family='Arial', size=fsss)
font_properties_legend = fm.FontProperties(family='Arial', size=fss)

C_INT, C_EXT, C_GRAY, C_BLUE, C_GOLD = '#77AEB3', '#E5885D', '#C7C4B5', '#A1C2DE', '#B4944B'
MARKER = {'GP-Matern': 'o', 'GP-ARD': 'o', 'GP': 'o', 'TabPFN': 's', 'HistGB': 's',
          'Ridge': '^', 'KRR-RBF': '^'}
FAMILY = {'GP-Matern': 'GP family', 'GP-ARD': 'GP family', 'GP': 'GP family',
          'TabPFN': 'tree boosting', 'HistGB': 'tree boosting',
          'Ridge': 'linear models', 'KRR-RBF': 'linear models'}
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures')
os.makedirs(OUT, exist_ok=True)


def apply_font_styling(ax):
    for tick in ax.get_xticklabels():
        tick.set_fontproperties(font_properties_tick)
    for tick in ax.get_yticklabels():
        tick.set_fontproperties(font_properties_tick)


def format_axis_labels(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel, fontproperties=font_properties_label)
    ax.set_ylabel(ylabel, fontproperties=font_properties_label)
    apply_font_styling(ax)


def legend_outside(ax, **kw):
    return ax.legend(prop=font_properties_legend, frameon=False, loc='upper left',
                     bbox_to_anchor=(1.02, 1.0), **kw)


def save_plot(fig, filename, dpi=300):
    fig.savefig(os.path.join(OUT, filename), dpi=dpi, bbox_inches='tight', format='svg')


def audit(fig, margin=2.0):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    texts, bad_frame = [], []
    for a in fig.get_axes():
        axbb = a.get_window_extent(renderer=renderer)
        for t in a.texts:
            if t.get_text().strip():
                texts.append(t)
                bb = t.get_window_extent(renderer=renderer)
                if bb.x0 < axbb.x0 - 1 or bb.x1 > axbb.x1 + 1 or bb.y0 < axbb.y0 - 1 or bb.y1 > axbb.y1 + 1:
                    bad_frame.append(t.get_text()[:30])
        if a.get_xlabel():
            texts.append(a.xaxis.label)
        if a.get_ylabel():
            texts.append(a.yaxis.label)
        texts.extend(a.get_xticklabels() + a.get_yticklabels())
    boxes = []
    for t in texts:
        if not t.get_text().strip():
            continue
        bb = t.get_window_extent(renderer=renderer)
        boxes.append((t, bb.expanded(1 + margin / bb.width if bb.width else 1,
                                     1 + margin / bb.height if bb.height else 1)))
    over = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes[i][1].overlaps(boxes[j][1]):
                over.append((boxes[i][0].get_text()[:25], boxes[j][0].get_text()[:25]))
    print('AUDIT overlaps:', over if over else 'none', '| frame overflow:',
          bad_frame if bad_frame else 'none')
    return over, bad_frame
