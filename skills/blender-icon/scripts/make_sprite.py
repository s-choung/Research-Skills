"""Pack motion frames into one sprite strip and write a matching still icon.

Usage: python make_sprite.py <frames_dir> <out_dir> [name ...] [--cell 256] [--still last|first] [--webp]

Input : <frames_dir>/NAME_f00.png .. NAME_fNN.png (from icon_kit.py with FRAMES=N)
Output: <out_dir>/spin_NAME.png  frames side by side, one square cell each
        <out_dir>/NAME.png       still icon cut with the same crop, so sprite and still line up

All frames share one crop box, so the icon does not jump between frames. The shadow is faded out before it
reaches the cell edge.
"""
import argparse
import glob
import os
import re
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out")
ap.add_argument("names", nargs="*")
ap.add_argument("--cell", type=int, default=256)
ap.add_argument("--still", choices=["last", "first"], default="last", help="motion icons rest on the last frame, spin icons on the first")
ap.add_argument("--webp", action="store_true", help="write the sprite as WebP (smaller) instead of PNG")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)


def fade(path):
    """Keep the object, fade the soft shadow to zero away from the object's foot."""
    im = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32)
    h, w = im.shape[:2]
    al = im[..., 3]
    ys, xs = np.nonzero(al >= 250)
    if len(xs) == 0:
        return Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cx, cy = xs.mean(), ys.max() - 0.05 * h
    rx, ry = (xs.max() - xs.min()) / 2, (ys.max() - ys.min()) / 2
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - cx) / (rx * 1.9 + 1)) ** 2 + ((yy - cy) / (ry * 1.2 + 1)) ** 2)
    t = np.clip((1.0 - d) / 0.55, 0, 1)
    im[..., 3] = np.where(al >= 250, al, al * t * t * (3 - 2 * t))
    return Image.fromarray(im.clip(0, 255).astype(np.uint8), "RGBA")


names = a.names or sorted({re.sub(r"_f\d+\.png$", "", os.path.basename(p)) for p in glob.glob(os.path.join(a.src, "*_f00.png"))})
for name in names:
    paths = sorted(glob.glob(os.path.join(a.src, name + "_f[0-9][0-9].png")))
    if not paths:
        print("skip (no frames)", name)
        continue
    frames = [fade(p) for p in paths]
    w, h = frames[0].size
    box = [w, h, 0, 0]
    for f in frames:
        bb = f.getchannel("A").point(lambda v: 255 if v > 2 else 0).getbbox()
        if bb:
            box = [min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3], bb[3])]
    side = max(box[2] - box[0], box[3] - box[1]) + 8
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
    crop = (cx - side // 2, cy - side // 2, cx - side // 2 + side, cy - side // 2 + side)
    sheet = Image.new("RGBA", (a.cell * len(frames), a.cell), (0, 0, 0, 0))
    for k, f in enumerate(frames):
        sheet.paste(f.crop(crop).resize((a.cell, a.cell), Image.LANCZOS), (a.cell * k, 0))
    if a.webp:
        sp = os.path.join(a.out, "spin_%s.webp" % name)
        sheet.save(sp, quality=90, method=6)
    else:
        sp = os.path.join(a.out, "spin_%s.png" % name)
        sheet.save(sp, optimize=True)
    still = frames[-1 if a.still == "last" else 0]
    still.crop(crop).resize((a.cell, a.cell), Image.LANCZOS).save(os.path.join(a.out, name + ".png"), optimize=True)
    print("ok", name, len(frames), "frames", "%d KB" % (os.path.getsize(sp) // 1024), flush=True)
