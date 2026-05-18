---
name: blender-atom-render
description: Render atomic structures and individual atom spheres using Blender's io_mesh_atomic addon. Two modes - (1) full-structure auto-frame rendering with multi-angle support, (2) single-atom sphere rendering for legends. Triggers - /blender-atom-render, "atom render", "원자 렌더링", "atom legend", "레전드 만들어", "blender로 렌더", "구 렌더링", "structure render blender"
---

# Blender Atom Render

Render atomic structures (molecules, slabs, nanoparticles, MOFs) and individual atom spheres using Blender's `io_mesh_atomic` addon.

## Prerequisites

- Blender installed at `/Applications/Blender.app/Contents/MacOS/Blender`
- Python with ASE (`ase`) and Pillow (`PIL`) in base conda
- For single-atom mode: a Blender `.blend` file with camera and lighting setup
- For full-structure mode: no .blend file needed (auto-frame script creates camera+lights)

## Mode 1: Full-Structure Auto-Frame Rendering

Renders complete structures (.xyz, .cif) with automatic camera framing, multi-angle support, and 3-point lighting. No .blend file required.

### Anti-clipping rules (CRITICAL)
- `ortho_scale = max_bounding_box_dim * 1.8` prevents edge clipping
- Never use `* 1.4` or lower; atoms at slab edges will be cut off
- For very flat slabs (z << x,y), use `max(size.x, size.y) * 1.6` instead of max_dim

### Camera angles
- **perspective**: 45-degree oblique view `(0.55, -0.55, 0.5)` normalized from center. Best for 3D structures (nanoparticles, MOFs).
- **top**: near-vertical `(0.15, -0.15, 0.95)`. Best for surface slabs to show top-layer pattern.
- Always render BOTH angles for each structure.

### Lighting: 3-point setup
- **Key light** (SUN, energy=3.5, angle=8deg): main illumination from upper-right
- **Fill light** (SUN, energy=1.2): softer from opposite side, reduces harsh shadows
- **Rim light** (SUN, energy=1.5): backlight for edge definition and depth

### Auto-frame render script
```python
# render_autoframe_v2.py
# Usage: blender --background --python render_autoframe_v2.py -- input.xyz output.png [perspective|top]
import bpy, sys, mathutils, math

argv = sys.argv[sys.argv.index("--") + 1:]
xyz_path = argv[0]
output_path = argv[1]
angle = argv[2] if len(argv) > 2 else "perspective"

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
bpy.ops.outliner.orphans_purge(do_recursive=True)

bpy.ops.preferences.addon_enable(module="io_mesh_atomic")
bpy.ops.import_mesh.xyz(
    filepath=xyz_path, ball="1", mesh_azimuth=128, mesh_zenith=128,
    scale_ballradius=1.0, scale_distances=1.0,
)

mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not mesh_objs: sys.exit(1)

all_min = mathutils.Vector((1e9, 1e9, 1e9))
all_max = mathutils.Vector((-1e9, -1e9, -1e9))
for obj in mesh_objs:
    for corner in obj.bound_box:
        world_pt = obj.matrix_world @ mathutils.Vector(corner)
        all_min.x = min(all_min.x, world_pt.x)
        all_min.y = min(all_min.y, world_pt.y)
        all_min.z = min(all_min.z, world_pt.z)
        all_max.x = max(all_max.x, world_pt.x)
        all_max.y = max(all_max.y, world_pt.y)
        all_max.z = max(all_max.z, world_pt.z)

center = (all_min + all_max) / 2
size = all_max - all_min
max_dim = max(size.x, size.y, size.z)

cam_data = bpy.data.cameras.new("AutoCam")
cam_data.type = 'ORTHO'
cam_data.ortho_scale = max_dim * 1.8  # 1.8x for safe margin

cam_obj = bpy.data.objects.new("AutoCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_dist = max_dim * 3

if angle == "top":
    cam_obj.location = center + mathutils.Vector((cam_dist*0.15, -cam_dist*0.15, cam_dist*0.95))
else:  # perspective
    cam_obj.location = center + mathutils.Vector((cam_dist*0.55, -cam_dist*0.55, cam_dist*0.5))

direction = center - cam_obj.location
cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam_obj

# 3-point lighting
for name, energy, loc, rot in [
    ("Key", 3.5, (cam_dist, -cam_dist, cam_dist*1.5), (30, 0, -45)),
    ("Fill", 1.2, (-cam_dist, cam_dist*0.5, cam_dist*0.3), (60, 0, 135)),
    ("Rim", 1.5, (-cam_dist*0.3, cam_dist*0.8, cam_dist*0.6), (45, 0, 180)),
]:
    light = bpy.data.lights.new(name, type='SUN')
    light.energy = energy
    obj = bpy.data.objects.new(name, light)
    bpy.context.collection.objects.link(obj)
    obj.location = center + mathutils.Vector(loc)
    obj.rotation_euler = tuple(math.radians(a) for a in rot)

bpy.context.scene.render.resolution_x = 2000
bpy.context.scene.render.resolution_y = 2000
bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)
```

### Batch rendering workflow
1. Render each file as a SEPARATE Blender process (no loops within Blender)
2. Always render both angles: `_perspective.png` and `_top.png`
3. Large structures (1000+ atoms): timeout 120s per render, ~15s typical
4. MOFs (500+ atoms): may need 30-60s

## Mode 2: Single-Atom Sphere Rendering (for legends)

## Workflow

### Step 1: Extract unique atoms from structure files

Use ASE to read all structure files and extract unique chemical symbols. Create single-atom XYZ files at (0,0,0).

```python
from ase.io import read
from ase import Atoms
from ase.io import write
import glob, os

traj_files = glob.glob('**/*.traj', recursive=True)
all_symbols = set()
for f in traj_files:
    atoms = read(f, index=-1)
    all_symbols.update(atoms.get_chemical_symbols())

for symbol in sorted(all_symbols):
    atom = Atoms(symbol, positions=[(0, 0, 0)])
    write(f'{symbol}.xyz', atom)
```

### Step 2: Create a clean blend file (camera + lights only)

Copy the original blend file, removing all mesh objects while preserving camera and lighting. Add a close-up orthographic camera for single-atom rendering.

**Key: use `bpy.data.objects.remove()` instead of `select_set() + delete`** — some objects may not be in the active ViewLayer and will fail with select-based deletion.

```python
# make_clean_blend.py — run with: blender original.blend --background --python make_clean_blend.py
import bpy, mathutils

OUTPUT_BLEND = "camera_light_clean.blend"

# Delete all non-camera/light objects via data API (bypasses ViewLayer issues)
keep_types = {'CAMERA', 'LIGHT', 'EMPTY'}
to_delete = [obj for obj in bpy.data.objects if obj.type not in keep_types]
for obj in to_delete:
    bpy.data.objects.remove(obj, do_unlink=True)
bpy.ops.outliner.orphans_purge(do_recursive=True)

# Add close-up orthographic camera for single atom
cam_data = bpy.data.cameras.new("AtomCam")
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 4.0  # adjust to frame atom nicely
cam_obj = bpy.data.objects.new("AtomCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (5.0, -5.0, 3.5)
direction = mathutils.Vector((0, 0, 0)) - cam_obj.location
cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam_obj

bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
```

### Step 3: Render each atom INDEPENDENTLY

**Critical lesson learned:** Rendering in a loop within a single Blender session causes material contamination — `_ball` objects persist across iterations despite deletion attempts. **Always launch a separate Blender process per atom.**

#### Default CPK colors

```python
# render_single.py — run with: blender clean.blend --background --python render_single.py -- input.xyz output.png
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:]
xyz_path, output_path = argv[0], argv[1]

bpy.ops.preferences.addon_enable(module="io_mesh_atomic")
bpy.ops.import_mesh.xyz(
    filepath=xyz_path,
    ball="1",             # '0'=NURBS, '1'=MESH, '2'=META
    mesh_azimuth=128,     # high = smoother sphere
    mesh_zenith=128,
    scale_ballradius=1.0,
    scale_distances=1.0,
)

bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)
```

#### Custom RGB colors

```python
# render_single_color.py — run with: blender clean.blend --background --python render_single_color.py -- input.xyz output.png R G B
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:]
xyz_path, output_path = argv[0], argv[1]
r, g, b = float(argv[2]), float(argv[3]), float(argv[4])

bpy.ops.preferences.addon_enable(module="io_mesh_atomic")
bpy.ops.import_mesh.xyz(
    filepath=xyz_path,
    ball="1",
    mesh_azimuth=128,
    mesh_zenith=128,
    scale_ballradius=1.0,
    scale_distances=1.0,
)

# Override material color on the ball object
for obj in bpy.context.scene.objects:
    if "_ball" in obj.name:
        if obj.data.materials:
            mat = obj.data.materials[0]
            mat.diffuse_color = (r, g, b, 1.0)
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        node.inputs['Base Color'].default_value = (r, g, b, 1.0)
        break

bpy.context.scene.render.filepath = output_path
bpy.ops.render.render(write_still=True)
```

Shell loop (custom colors via function):

```bash
BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
render_atom() {
  local elem=$1 r=$2 g=$3 b=$4
  "$BLENDER" "$CLEAN_BLEND" --background --python render_single_color.py -- \
    "${elem}.xyz" "renders/${elem}.png" "$r" "$g" "$b"
}

render_atom Ba  0    0.78  0
render_atom La  0.502 0.922 0.973
# ... etc. RGB values are floats 0.0-1.0
```

Shell loop (default CPK colors):

```bash
for xyz in input_dir/*.xyz; do
    elem=$(basename "$xyz" .xyz)
    "$BLENDER" "$CLEAN_BLEND" --background --python render_single.py -- "$xyz" "renders/${elem}.png"
done
```

### Step 4: Create per-system legend images

Use Pillow to compose horizontal legends with rendered 3D sphere PNGs as icons: `[rendered sphere] Name  [rendered sphere] Name  ...`

```python
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = '/System/Library/Fonts/Supplemental/Arial.ttf'
ICON_SIZE = 60     # rendered sphere resized to this
FONT_SIZE = 48
SPACING = 10       # gap between icon and text
ITEM_GAP = 40      # gap between pairs
PADDING_X = 30

systems = {
    'BCZYYb-GCCCO': ['Ba', 'Ca', 'Ce', 'Co', 'Cu', 'Gd', 'O', 'Y', 'Yb', 'Zr'],
    'GDC-GCCCO':    ['Ca', 'Ce', 'Co', 'Cu', 'Gd', 'O'],
    'GDC-LSCF':     ['Ce', 'Co', 'Fe', 'Gd', 'La', 'O', 'Sr'],
}

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

for sys_name, elements in systems.items():
    items_widths = []
    for elem in elements:
        bbox = font.getbbox(elem)
        items_widths.append(ICON_SIZE + SPACING + bbox[2] - bbox[0])

    total_w = PADDING_X * 2 + sum(items_widths) + ITEM_GAP * (len(elements) - 1)
    total_h = max(ICON_SIZE + 20, 100)

    img = Image.new('RGBA', (total_w, total_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    x = PADDING_X
    cy = total_h // 2

    for elem in elements:
        # Use rendered 3D sphere as icon
        sphere = Image.open(f'renders/{elem}.png').convert('RGBA')
        sphere = sphere.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
        img.paste(sphere, (x, cy - ICON_SIZE // 2), sphere)

        bbox = font.getbbox(elem)
        th = bbox[3] - bbox[1]
        ty = cy - th // 2 - bbox[1]
        draw.text((x + ICON_SIZE + SPACING, ty), elem, fill=(0, 0, 0, 255), font=font)

        tw = bbox[2] - bbox[0]
        x += ICON_SIZE + SPACING + tw + ITEM_GAP

    img.save(f'renders/legend_{sys_name}_v2_WJ.png', 'PNG')
```

For a merged legend with all atoms: collect `sorted(set(...))` of all atoms across systems and generate one combined image (`legend_v2_WJ.png`).

## Important Notes

### io_mesh_atomic API quirks
- `ball` parameter uses string enums: `'0'`=NURBS, `'1'`=MESH, `'2'`=META (NOT `'MESH'` etc.)
- `use_camera`, `use_light` parameters may not exist in some Blender versions — omit them
- Each element gets its own Principled BSDF material with CPK-style colors automatically

### Object cleanup pitfalls
- `bpy.ops.object.select_set()` fails for objects not in the active ViewLayer
- Use `bpy.data.objects.remove(obj, do_unlink=True)` for reliable deletion
- `_ball` objects from `io_mesh_atomic` tend to persist — separate processes are the safest solution

### Camera for single atoms
- Original blend cameras are typically set for large structures (ortho_scale 14-300)
- Single atoms need ortho_scale ~3-5 depending on element radius
- Ortho cameras: distance doesn't matter, only `ortho_scale` controls framing

### Mesh smoothness
- `mesh_azimuth` and `mesh_zenith` control sphere polygon count
- 32x32 = visibly faceted, 64x64 = acceptable, 128x128 = smooth sphere
