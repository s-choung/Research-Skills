"""Figure 1 (integrated): 3-B free-energy diagram with circular molecule insets
per state, gas reactant/product renders at both ends."""
import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import numpy as np

matplotlib.rcParams['mathtext.default'] = 'regular'
BASE = ("/Users/sean/Library/CloudStorage/GoogleDrive-wjdtjrgus9967@gmail.com/"
        "My Drive/Research_2026/playground/186_Grace_Wang_cowork")
R = f"{BASE}/renders"
dG = json.load(open(f"{BASE}/results/dG_levels_campbell.json"))

COL = '#6a5acd'
fp_ann = fm.FontProperties(family='Arial', size=13.5)
fp_gas = fm.FontProperties(family='Arial', size=12)
fp_label = fm.FontProperties(family='Arial', size=18)
fp_tick = fm.FontProperties(family='Arial', size=16)


def mol_circle(name, gasmode=False, size=460, out_px=400, ox=0, oy=0):
    """Square crop centered on the carbon atoms (dark-pixel centroid + per-system
    (ox, oy) tweak, render px), radial alpha fade. Gas renders: plain crop, no fade."""
    im = Image.open(f"{R}/{name}.png").convert('RGBA')
    a = np.asarray(im).astype(float)
    alpha = a[..., 3]
    if gasmode:
        ys, xs = np.nonzero(alpha > 40)
        b = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        crop = a[b[1]:b[3], b[0]:b[2]]
        sc = out_px / max(crop.shape[:2])
        img = Image.fromarray(crop.astype(np.uint8))
        img = img.resize((int(crop.shape[1] * sc), int(crop.shape[0] * sc)),
                         Image.LANCZOS)
        return np.asarray(img)
    lum = a[..., :3].mean(axis=2)
    dark = (lum < 90) & (alpha > 40)
    ys, xs = np.nonzero(dark)
    cx, cy = np.median(xs) + ox, np.median(ys) + oy
    h, w = alpha.shape
    half = size
    x0, x1 = int(cx - half), int(cx + half)
    y0, y1 = int(cy - half), int(cy + half)
    pad = [max(0, -x0), max(0, x1 - w), max(0, -y0), max(0, y1 - h)]
    crop = a[max(0, y0):min(h, y1), max(0, x0):min(w, x1)]
    if any(pad):
        crop = np.pad(crop, ((pad[2], pad[3]), (pad[0], pad[1]), (0, 0)))
    n = crop.shape[0]
    yy, xx = np.mgrid[0:n, 0:crop.shape[1]]
    r = np.hypot(xx - crop.shape[1] / 2, yy - n / 2) / (n / 2)
    fade = np.clip((1.0 - r) / 0.28, 0, 1)      # opaque inside r<0.72, cos fade out
    fade = 0.5 - 0.5 * np.cos(np.pi * fade)
    crop[..., 3] = crop[..., 3] * fade
    img = Image.fromarray(crop.astype(np.uint8)).resize((out_px, out_px),
                                                        Image.LANCZOS)
    return np.asarray(img)


# (key, label, side, render, gasmode, label_dy, inset_dy_extra, inset_dx,
#  fade-center tweak (ox, oy) in render px, seg on incoming connector)
STATES = [
    ('ZERO',      'H* + 2 CH$_3$COOH(g)',                        'below', 'gas_2acoh_fs',            True,  0, 10,  0.00, (0, 0), ''),
    ('h_acoh',    'CH$_3$COOH* + H*',                            'above', 'H_B0_AcOH_nobox_top',     False, 0,  0,  0.00, (-140, 30), ''),
    ('h_acyl_md', 'CH$_3$CO*',                                   'below', 'acyl_true_nobox_top',     False, 0, 16,  0.00, (0, 0), '+ H$_2$O(g)'),
    ('h_pair3',   'CH$_3$COOH*\n+ CH$_3$CO*',                    'above', 'pair3_shift_ab2_nobox_top', False, 0, 2,  0.00, (0, 0), '+ CH$_3$COOH(g)'),
    ('h_pair4',   'CH$_3$COO*\n+ CH$_3$CO* + H*',                'below', 'pair4_alt2_nobox_top',    False, 0,  8,  0.00, (60, -100), ''),
    ('h_acac2h',  'CH$_3$COCH$_2$COO*\n+ 2 H*',                  'above', 'acac2h_n1_nobox_top',     False, 0, 14, -0.30, (-200, 20), ''),
    ('h_co2s2h',  'CO$_2$* + CH$_2$C(CH$_3$)O*\n+ 2 H*',         'above', 'co2s2h_n1_nobox_top',     False, 0,  8,  0.10, (0, 0), ''),
    ('h_acetone', 'CH$_3$COCH$_3$* + H*',                        'below', 'H_A8_acetone_nobox_top',  False, 0,  8,  0.00, (-70, 20), '+ CO$_2$(g)'),
    ('h_products','CH$_3$COCH$_3$(g) + H*\n+ CO$_2$(g) + H$_2$O(g)', 'below', 'gas_products_fs',     True,  0, 46,  0.00, (0, 0), ''),
]
HW = 0.42
ZOOM = 0.36          # inset display scale (of the 400-px circle)
INSET_KJ = 72.0      # distance from label block to inset center, kJ units

fig, ax = plt.subplots(figsize=(18.0, 9.6))
xs = list(range(len(STATES)))
ys = [0.0 if s[0] == 'ZERO' else dG[s[0]] for s in STATES]

for i, (key, lab, side, render, gasmode, ldy, idy, idx, (ox, oy), seg) in enumerate(STATES):
    x, y = xs[i], ys[i]
    ax.hlines(y, x - HW, x + HW, color=COL, linewidth=3.5)
    if i:
        x0, y0 = xs[i - 1], ys[i - 1]
        ax.plot([x0 + HW, x - HW], [y0, y], color=COL, linewidth=1.2, alpha=0.85)
        if seg:
            ax.annotate(seg, xy=(x0 + 0.5 * (x - x0), y0 + 0.5 * (y - y0)),
                        ha='center', va='center', fontproperties=fp_gas,
                        color='#5a6573',
                        bbox=dict(facecolor='white', alpha=0.6,
                                  edgecolor='none', pad=1.5))
    off = (8 + ldy) if side == 'above' else -(8 + ldy)
    ax.annotate(lab, xy=(x, y), xytext=(x, y + off), ha='center',
                va='bottom' if side == 'above' else 'top',
                fontproperties=fp_ann, color='#1a1a1a')
    nlines = lab.count('\n') + 1
    ins = INSET_KJ + idy + (nlines - 1) * 16
    iy = y + off + (ins if side == 'above' else -ins)
    size = 500 if key == 'h_pair4' else 460   # pair4: two PBC fragments, wider crop
    img = mol_circle(render, gasmode=gasmode, ox=ox, oy=oy, size=size)
    ab = AnnotationBbox(OffsetImage(img, zoom=ZOOM), (x + idx, iy),
                        frameon=False, box_alignment=(0.5, 0.5), zorder=3)
    ax.add_artist(ab)

# largest uphill step highlight
ups = [(ys[i] - ys[i - 1], i) for i in range(1, len(ys))]
dmax, imax = max(ups)
x1, y1, x2, y2 = xs[imax - 1], ys[imax - 1], xs[imax], ys[imax]
ax.fill_between([x1 + HW, x2 - HW], min(y1, y2), max(y1, y2),
                color='#D64550', alpha=0.15, linewidth=0, zorder=0.5)
ax.annotate(f'+{dmax:.0f} kJ/mol', xy=((x1 + x2) / 2, (y1 + y2) / 2),
            ha='center', va='center', fontproperties=fp_ann, color='#D64550',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=1.5))

ax.axhline(0, color='#cccccc', linewidth=0.7, zorder=0)
ax.set_xlim(-0.95, len(STATES) - 1 + 0.95)
ax.set_ylim(-215, 265)
ax.set_xticks([])
ax.set_xlabel('Reaction coordinate', fontproperties=fp_label)
ax.set_ylabel('$\\Delta$G$_{523}$ (kJ/mol)', fontproperties=fp_label)
for t in ax.get_yticklabels():
    t.set_fontproperties(fp_tick)
plt.subplots_adjust(left=0.06, right=0.99, top=0.98, bottom=0.07)
fig.savefig(f"{BASE}/output/fig1_integrated_3B.png", dpi=220,
            facecolor='white')
print('SAVED fig1_integrated_3B.png')
