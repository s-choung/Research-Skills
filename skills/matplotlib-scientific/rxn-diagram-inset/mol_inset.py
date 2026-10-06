"""Circular fade insets of Blender structure renders for reaction diagrams.

mol_circle(path, ...)  -> RGBA ndarray, molecule-centered circular fade crop
                          (surface renders) or plain alpha-bbox crop (gas).
add_inset(ax, img, x, y, zoom) -> AnnotationBbox placed at data coords.

Proven on Fig 1 of the CeO2 ketonization manuscript (2026-09). Key lessons:
- Automatic dark-pixel centroids get dragged toward the surface shadow
  crevices; ALWAYS expose per-system (ox, oy) manual tweaks (render px)
  and iterate visually (render -> Read the PNG -> adjust).
- Keep (cx +- size) inside the render frame or the circle gets a flat
  clipped edge; reduce |oy| or size instead of padding.
- Gas-phase renders: no fade (plain crop), per user preference.
"""
import numpy as np
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def mol_circle(path, gasmode=False, size=460, out_px=400, ox=0, oy=0):
    """Crop centered on the carbon atoms (dark-pixel median + (ox, oy) tweak,
    render px), radial cos alpha fade (opaque r<0.72, fade to 0 at edge).
    gasmode=True: plain alpha-bbox crop, no fade."""
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im).astype(float)
    alpha = a[..., 3]
    if gasmode:
        ys, xs = np.nonzero(alpha > 40)
        crop = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
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
    x0, x1 = int(cx - size), int(cx + size)
    y0, y1 = int(cy - size), int(cy + size)
    pad = [max(0, -x0), max(0, x1 - w), max(0, -y0), max(0, y1 - h)]
    crop = a[max(0, y0):min(h, y1), max(0, x0):min(w, x1)]
    if any(pad):
        crop = np.pad(crop, ((pad[2], pad[3]), (pad[0], pad[1]), (0, 0)))
    n = crop.shape[0]
    yy, xx = np.mgrid[0:n, 0:crop.shape[1]]
    r = np.hypot(xx - crop.shape[1] / 2, yy - n / 2) / (n / 2)
    fade = np.clip((1.0 - r) / 0.28, 0, 1)
    fade = 0.5 - 0.5 * np.cos(np.pi * fade)
    crop[..., 3] = crop[..., 3] * fade
    img = Image.fromarray(crop.astype(np.uint8)).resize((out_px, out_px),
                                                        Image.LANCZOS)
    return np.asarray(img)


def add_inset(ax, img, x, y, zoom=0.36):
    ab = AnnotationBbox(OffsetImage(img, zoom=zoom), (x, y),
                        frameon=False, box_alignment=(0.5, 0.5), zorder=3)
    ax.add_artist(ab)
    return ab
