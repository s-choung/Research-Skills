---
name: blender-icon
description: Make clay-style 3D icons with looping motions for web pages, built from primitive shapes in Blender (bpy) and packed into sprite strips. Use for icon sets, card thumbnails, hover or autoplay motions, and chemistry icons with ball-and-stick molecules. Triggers - blender icon, 3D icon, icon motion, hover animation, sprite strip, clay icon, molecule icon, 아이콘 만들어, 3D 아이콘, 아이콘 모션.
---

# blender-icon: 3D icons and their motions

One icon is one Python function. A motion is the same function with a phase `t` from 0 to 1 as input.
The function rebuilds the whole scene at each phase, so Blender keyframes are not used.
Every motion ends at `t = 1` in the resting pose, which is also the still icon.

Live examples: https://schoung.com/resource/blender_icon

## Files

| File | Content |
|---|---|
| `scripts/icon_kit.py` | Scene setup, materials, primitives, ball-and-stick molecules, motion helpers, three example icons, render loop |
| `scripts/make_sprite.py` | Packs frames into one sprite strip and writes a still icon with the same crop |
| `prompts/general.md` | General prompt with two blanks, one sentence for the icon and one for the motion |
| `prompts/*.md` | Nine example prompts for chemistry icons |

Requirements: Blender 3.6 or later (`brew install --cask blender`), Python with `numpy` and `pillow` for the sprite script.

## Scene rules

- Cycles, 96 samples, denoising, transparent film, view transform `Standard`.
- Orthographic camera, `ortho_scale` 4.1, from the front and slightly above. Axes: x right, z up, -y toward the camera.
- Build the icon inside x from -1 to 1 and z from 0 to 2. If it overflows, lower the scale in `ICONS`.
- The floor is a shadow catcher, so only a soft shadow remains. Lighting is two suns (key 2.6, fill 0.6).
- Use the palette constants only: `NAVY`, `GREEN`, `LIME`, `ORANGE`, `WHITE`, `GRAY`, `DARK`, `GOLD`, `RED`, `BLUE`, `SILVER`. Materials come from `M(colour, roughness)`.
- Every box goes through `rbox`, which bevels the edges. Round edges give the clay look.

## Making an icon

1. Write one sentence on what the icon shows. Example: "A hand with the palm up and a methanol molecule above the palm." Three to fifteen parts are enough.
2. Write `p_NAME()` in `icon_kit.py`. It creates the parts and returns them as a list.
   - `rbox((width, depth, height), bevel, M(colour), loc=, rot=)`
   - `sph(r, M(colour), loc)`, `cyl(r, height, M(colour), loc=, r2=top radius)`, `cyl_between(p1, p2, r, M(colour), r2=)`
   - `torus(R, r, M(colour), loc, rot=)`, `prism([(x, z), ...], y0, y1, M(colour))`
   - `molecule(spec, centre, scale, tilt=)` draws a ball-and-stick molecule. `WATER`, `METHANOL` and `ETHANOL` are included. A new molecule is a list of `(element, x, y, z)` in angstrom and a list of bonded index pairs.
3. Register it in `ICONS` as `"name": (p_NAME, "spin", yaw, scale)`.
4. Render one still and look at the image. Check overlap, clipping and colour contrast, then fix.

## Making a motion

A plain turn makes every icon feel the same. Choose the action that carries the meaning of the icon.

1. Write the motion in one sentence. Example: "The hand starts as a fist, the fingers open, and methanol pops up."
2. Write `a_NAME(t)`. It builds the scene at phase `t`.
   - `seg(t, a, b)` goes from 0 to 1 while `t` goes from `a` to `b`. Give each part its own time window.
   - `ease(x)` gives smooth acceleration and deceleration. `back(x)` overshoots slightly and returns.
   - `xf(parts, s=, pivot=, rot=, loc=)` scales and rotates about a pivot and then shifts. Use it for hinges such as lids, fingers and book covers.
   - `pop(build, k, pivot, drop=)` makes a group grow in about a pivot. With `drop` it falls from above.
   - `star(loc, size)` is a sparkle. Multiply the size by `math.sin(math.pi * seg(...))` so that it appears and vanishes.
3. Keep three rules.
   - `t = 1` is the resting pose. A motion that opens and closes has the same pose at `t = 0` and `t = 1`.
   - At least one part is visible at `t = 0`. Start the first window slightly below zero, for example `seg(t, -0.05, 0.15)`.
   - Parts stay near the frame. The sprite uses one crop for all frames, so a part that flies far away makes the icon small.
4. Register it as `"name": (a_NAME, "motion", yaw, scale)`.
5. Render a low-resolution preview first and look at every frame on one sheet. Check the order and check that no part overlaps or vanishes in the middle.
6. Show the preview to the user. Render the final frames only after approval.

### Motion types

| Type | Examples | Method |
|---|---|---|
| Parts appear in order | bar chart, periodic table, network nodes | shift the `seg` window of each part and `pop` |
| A line grows | network edges, bonds | `cyl_between(a, lerp(a, b, k))` |
| Hinge | fist opening, book cover, lid, wand | `xf(..., pivot=hinge, rot=angle * k)` |
| Path | ball on an energy profile, juggled molecules, robot gripper | position as a function of `t` |
| Sparkle | completion, magic | `star` size times a sine |
| Turn | crystal cell, atom, laptop | kind `"spin"` |

## Running

Run one Blender process at a time.

```
# still icons, 512 px
ONLY=hand,crystal blender -b -P scripts/icon_kit.py -- out 512

# motion preview: 12 frames, 160 px, 20 samples
FRAMES=12 SAMPLES=20 THREADS=4 blender -b -P scripts/icon_kit.py -- preview 160
python scripts/make_sprite.py preview preview_web --cell 160

# final: 24 frames, 512 px
FRAMES=24 SAMPLES=48 THREADS=6 blender -b -P scripts/icon_kit.py -- frames 512
python scripts/make_sprite.py frames web --cell 384 --webp
```

`SKIP=1` keeps frames that already exist. On macOS the binary is `/Applications/Blender.app/Contents/MacOS/Blender`.
A final frame takes about 10 s at 512 px on a laptop CPU, so run the final render in the background and read only the `DONE` and `FAILED` lines.
For spin icons pass `--still first` to `make_sprite.py`.

## Web page

The sprite is one image with all frames side by side. CSS plays it without JavaScript.

```html
<div class="sp" style="background-image:url(web/spin_hand.webp)"></div>
<style>
.sp { width: 160px; aspect-ratio: 1 / 1; background-size: 2400% 100%; background-repeat: no-repeat;
      animation: play 2.6s steps(24, jump-none) infinite; }
@keyframes play { 0% { background-position: 0 0; } 70%, 100% { background-position: 100% 0; } }
@media (prefers-reduced-motion: reduce) { .sp { animation: none; background-position: 100% 0; } }
</style>
```

- `background-size` is the number of frames times 100%.
- The `70%, 100%` stop holds the resting pose before the loop restarts. For a spin icon use `0%` and `100%` only.
- Icons that share the same duration play in step.
- Display the sprite at half the cell size or smaller (a 384 px cell at 192 px). A larger display looks soft on high-density screens.

## Common problems

- A frame has no object: make a part visible at `t = 0`.
- The still icon and the first sprite frame differ in size: write both with `make_sprite.py`, which uses one crop.
- The shadow is cut at the image edge: the object is too large or too low. Lower the scale.
- A white object vanishes on a white page: put it next to a `NAVY` or `DARK` part.
- A part stays in place after moving it: use `xf`, which updates the view layer before changing `matrix_world`. Do not set `location` after parenting.

## Checklist

- [ ] Looked at the still render
- [ ] Looked at every motion frame on one sheet
- [ ] The frame at `t = 1` equals the still icon
- [ ] Showed the preview to the user before the final render
- [ ] Checked the motion on the actual page
