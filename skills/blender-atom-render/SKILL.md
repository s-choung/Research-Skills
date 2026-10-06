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

## Resource Management (CRITICAL - READ FIRST)

Blender Cycles and OVITO Tachyon are both CPU/GPU-intensive. Parallel rendering WILL crash on laptops (M1/M2 Mac, 16-32GB RAM).

### Rules
- **NEVER dispatch parallel subagents** for rendering. Each Blender/OVITO process uses 2-8GB RAM + full CPU.
- Batch renders in a **single sequential Python script** instead. Write one .py file that loops through all inputs, then run it as one `conda run` or Blender call.
- For Blender: max **1 process at a time**. Even 2 concurrent Blender instances can OOM on 16GB Mac.
- For OVITO: max **2-3 concurrent** (lighter than Blender, but still heavy for 500+ atom structures).
- Large structures (1000+ atoms, MOFs): set timeout=300000 and expect 30-60s per render.
- If rendering 20+ files: write a batch script, run in background, monitor with `tail`.

### Memory estimation
| Atoms | Blender RAM | OVITO RAM | Render time |
|-------|------------|-----------|-------------|
| < 50 | ~500 MB | ~200 MB | 1-3s |
| 100-300 | ~1 GB | ~500 MB | 5-15s |
| 500-1000 | ~2 GB | ~800 MB | 15-40s |
| 1000+ | ~4 GB | ~1.5 GB | 30-120s |

## Default: element legend accompanies every structure render (MANDATORY)

Whenever Mode 1 renders an atomic structure for the user (preview grid,
contact sheet, figure panel, HTML embed), ALSO produce an element legend by
default — rendered sphere icon + element name for every element present
(e.g. Ce, O, Co, Pt). The user should never have to ask for it (observed
failure 2026-07-10: a whole session of NP renders shipped legend-less until
the author demanded one).

- Build it from Mode 2 single-atom renders at **256 px** (see the low-res
  rule below) + the PIL legend composer in Step 4.
- **Cache** per-element sphere PNGs in the project's renders dir and reuse;
  re-render only when the element set or its material changes.
- If the structure render overrides a material (e.g. metallic Pt), render
  that element's legend sphere with the SAME override — legend must match
  the figure.
- Attach the legend into the composed output (bottom band of the grid) or
  save `legend.png` next to the renders when output is a bare PNG.
- Skip ONLY when the user explicitly declines, or for internal debug
  scatters that are not shown as renders.

## Mode 1: Full-Structure Auto-Frame Rendering

Renders complete structures (.xyz, .cif) with automatic camera framing, multi-angle support, and 3-point lighting. No .blend file required.

### Anti-clipping rules (CRITICAL)
- `ortho_scale = max_bounding_box_dim * 1.8` prevents edge clipping
- Never use `* 1.4` or lower; atoms at slab edges will be cut off
- For very flat slabs (z << x,y), use `max(size.x, size.y) * 1.6` instead of max_dim

### Ball radius rule (CRITICAL)
- Always use `scale_ballradius=1.0`. NEVER reduce below 1.0.
- Reducing ballradius (e.g., 0.35) makes atoms look disconnected, especially in MOFs/COFs where bond visualization depends on atom sphere overlap.
- If structure looks too crowded, zoom out (increase ortho_scale) instead of shrinking atoms.

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

### PBC cell box = the TRUE cell, vacuum included (MANDATORY, 2026-10-05 사용자 지시)
- The box is the real lattice: all three lattice vectors at full length. **Never cut or shrink the
  box to the extent of the atoms.** A slab or 2D sheet with 10-15 A of vacuum must show that vacuum:
  the box is much taller than the slab. A box that hugs the atoms along z is wrong (사용자 지적:
  "Z축이 너무 짧게 표현된다. 항상 그래").
- Do NOT derive the box from the atoms' bounding box. Step 2 below (`acenter ± L/2`) is only a
  workaround for the io_mesh_atomic re-centering and is wrong for slabs: it puts half of the vacuum
  below the slab. Preferred: place the spheres yourself at the file coordinates (no io_mesh_atomic)
  and draw the 12 edges from the lattice vectors at the file origin. The slab then sits where it
  sits in the file (normally at the bottom of the cell, vacuum above).
- Non-orthogonal cells: build the 8 corners as i*a + j*b + k*c, never as an axis-aligned Lx, Ly, Lz box.
- Frame the camera on the box corners plus the atoms, not on the atoms only.
- Check before delivering: box height along the vacuum axis == |c| of the file. Reference
  implementation: `217_catagentbench/render/xyz_to_json2.py` + `render_structs2.py`.

### PBC cell box wireframe (CRITICAL alignment rule)
**DEFAULT (2026-07-17): periodic structures (extxyz/cif with a lattice) get the cell
box wireframe by default.** Only skip when the structure is non-periodic (molecule,
nanoparticle) or the user explicitly declines. Plain .xyz drops the cell — export
**.extxyz** so the `Lattice=` line survives (V7 `viz_blender_autoframe.py` parses it
and draws the box automatically).
When drawing the periodic simulation cell as a wireframe, **center the box on the
imported atoms' bounding-box center — NOT on the file's [0,L] coords.** `io_mesh_atomic`
**re-centers the structure to the world origin** on import, so a box drawn at `[0,L]`
is offset by ~L/2 and floats away from the atoms (classic bug). Always:
1. import atoms, then compute their world-space bounds `amin/amax` → `acenter=(amin+amax)/2`.
2. draw the cell corners as `acenter ± (Lx/2, Ly/2, Lz/2)` (pass `Lx Ly Lz` as args).
3. render the 12 edges as thin **cylinders** (radius ~0.3-0.35) with a **BLACK matte
   material**: a near-black Principled BSDF (base `(0,0,0)`, Specular 0, Roughness ~0.8),
   NOT an emission. **Cell-box edges must be BLACK - never cyan/teal.** The old `#10a37f` teal glow reads
   as a distracting neon box and was explicitly rejected; a pure-black wireframe reads
   cleanly over both the atoms and a light figure background.
4. atoms should be **per-atom wrapped** into the cell first (`ase Atoms.wrap()`); since
   io_mesh_atomic draws balls only (no bonds), wrap-split molecules show no artifact —
   the box then encloses everything cleanly. (Molecule-whole wrap only matters if you
   draw bonds.)
```python
# after import, BEFORE camera: box centered on atoms (io_mesh_atomic centers to origin)
amin = mathutils.Vector((1e9,)*3); amax = mathutils.Vector((-1e9,)*3)
for o in [o for o in bpy.context.scene.objects if o.type=='MESH']:
    for c in o.bound_box:
        w = o.matrix_world @ mathutils.Vector(c)
        amin = mathutils.Vector((min(amin.x,w.x),min(amin.y,w.y),min(amin.z,w.z)))
        amax = mathutils.Vector((max(amax.x,w.x),max(amax.y,w.y),max(amax.z,w.z)))
ac = (amin+amax)/2; h = mathutils.Vector((Lx/2,Ly/2,Lz/2))
mat = bpy.data.materials.new("CellEdge"); mat.use_nodes=True; nt=mat.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
# BLACK cell edges: matte near-black Principled BSDF, NEVER a cyan/teal emission.
eb = nt.nodes.new("ShaderNodeBsdfPrincipled"); eb.inputs['Base Color'].default_value=(0,0,0,1)
eb.inputs['Metallic'].default_value=0.0; eb.inputs['Roughness'].default_value=0.8
if 'Specular IOR Level' in eb.inputs: eb.inputs['Specular IOR Level'].default_value=0.0
nt.links.new(eb.outputs[0], nt.nodes.new("ShaderNodeOutputMaterial").inputs[0])
corn = [ac+mathutils.Vector((sx*h.x,sy*h.y,sz*h.z)) for sx in(-1,1) for sy in(-1,1) for sz in(-1,1)]
for i in range(8):
    for j in range(i+1,8):
        if sum(1 for c in (corn[i]-corn[j]) if abs(c)>1e-6)==1:  # axis-aligned edge
            v=corn[j]-corn[i]; bpy.ops.mesh.primitive_cylinder_add(radius=0.33, depth=v.length, location=(corn[i]+corn[j])/2)
            cy=bpy.context.active_object; cy.rotation_euler=v.to_track_quat('Z','Y').to_euler(); cy.data.materials.append(mat)
```
For **movies** (frame sequence), additionally use a **FIXED camera** (`ortho_scale` from
the cell length, not per-frame bounding box) so the view doesn't jitter frame-to-frame.

### Batch rendering workflow
1. Render each file as a SEPARATE Blender process (no loops within Blender)
2. Always render both angles: `_perspective.png` and `_top.png`
3. Large structures (1000+ atoms): timeout 120s per render, ~15s typical
4. MOFs (500+ atoms): may need 30-60s

## Mode 2: Single-Atom Sphere Rendering (for legends)

### Legend icons are tiny — render them at LOW resolution (CRITICAL for file size)
Legend sphere icons display at ~24–60 px (an HTML `<img>` or Pillow `ICON_SIZE`).
Rendering them at full resolution (1000–2000 px, ~1.5 MB PNG each) is pure waste, and it
**balloons any HTML that base64-inlines them.** Real case (this project): 15 element spheres
re-embedded across 14 task-card legends = 82 icon embeds; at full res that was **165 MB of a
257 MB dashboard — almost all of it duplicated full-res sphere dots.** Quality does NOT matter
for a legend dot, only for Mode-1 full structures.

Fix either at render time or embed time:
- **Render small:** `scene.render.resolution_x = scene.render.resolution_y = 256` (128–256 is
  plenty for a legend dot — do NOT inherit Mode-1's 2000).
- **Or downscale at embed time:** `PIL Image.open(p).resize((96,96), Image.LANCZOS)` →
  `save(buf,"PNG",optimize=True)` → base64. (You don't even need to dedup the duplicates; once
  each icon is ~10 KB instead of ~1.5 MB, 82 copies total <1 MB.)

That single change took the dashboard from **257 MB → 4.5 MB** with zero visible loss at icon size.

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

## Reaction-Strip 렌더 (elementary step 시퀀스) — 2026-09 CeO2 케톤화 캠페인 규칙 (MANDATORY)

다이어그램(ΔG ladder)과 짝지어 elementary step 구조 strip을 만들 때의 하드 규칙.

1. **렌더 구조 = 에너지 소스 구조, 일대일 (최우선).** strip의 각 셀은 ΔG 다이어그램이 실제로 사용하는
   에너지의 구조 파일을 그대로 렌더해야 한다. 스크립트에 에너지 오버라이드(`e2[...]['E_eV'] = rc2[...]`)가
   있으면 렌더 대상도 오버라이드된 파일로 바꿀 것. 실사고: enum "acyl" 구조가 실제로는 탈양성자화된
   ketene+H(격자 O)였는데 렌더에 그대로 쓰여 사용자가 그림에서 화학 오류를 발견함. **strip 제작 전에
   에너지 소스 파일 목록을 뽑아 렌더 파일과 대조하는 audit를 먼저 돌릴 것** (fragment 조성 + H-격자O 결합 체크).
2. **라벨 = 상태 조성 전체.** H*가 포함된 상태면 라벨에도 `CH2CO* + H*`처럼 명시. 다이어그램 라벨과 어긋나면 안 됨.
3. **중간체 간 거리 질문 대비**: co-adsorbed pair의 최저 배치는 격자 이산성 때문에 4-5 Å(= O-O 최근접
   3.8 Å의 한 칸 옆)로 보인다. "인접 사이트" 서술 + near-vs-far 에너지 차이를 정량해 방어. 렌더를 숨기지 말 것.
4. **가스 타일**: (a) 렌더 자체의 edge-clipping을 `im.getbbox()`가 캔버스 경계에 닿는지로 전수 검사 —
   닿으면 ortho_scale 마진 부족. 작은 계(max_dim < 15 Å)는 top/side ortho에 x1.45 추가 마진.
   (b) strip 합성 시 crop에 pad 10px, 높이는 슬랩의 ~32%, **폭도 상한**(슬랩 높이의 ~55%) — side 뷰의
   납작한 분자가 높이 기준 리사이즈로 거대해지는 것 방지.
5. **버전 토글**: 경로 변형(lumped/int1/int2)별 strip을 각각 합성하고 HTML에서 (버전 x 시점) 2단 버튼 토글.
   base64 임베드는 폭 1200/1500/1400px 리사이즈 + quantize(255).

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

### Mesh smoothness & render speed (smooth is nearly free)
- `mesh_azimuth` / `mesh_zenith` set the ball polygon count: 32x32 = visibly
  faceted (flat-shaded), 64x64 = acceptable, 128x128 = smooth.
- **Why high subdivision is cheap:** io_mesh_atomic builds ONE `{Element}_ball`
  mesh per element and instances it at every atom via dupliverts (the
  `{Element}_mesh` parent, `instance_type='VERTS'`). Raising subdivision only
  enlarges a handful of ball meshes — it does NOT scale with atom count and
  barely changes render time. (The `_ball` object's `scale` == the atom radius,
  so you can match one element's radius to another by copying its `.scale`.)
- **The real cheap win is smooth shading** (normal interpolation, zero geometry
  cost). Flip every `_ball` to smooth after import; even 32x32 then looks round.
  Prefer moderate subdivision (48–64) + smooth shading over brute-forcing 128.
  ```python
  for o in bpy.context.scene.objects:
      if o.type == 'MESH' and o.name.endswith("_ball"):
          me = o.data
          for p in me.polygons:
              p.use_smooth = True      # flat -> smooth normals (free)
          me.update()
  ```
- **What actually costs render time** is resolution and sample count (EEVEE
  `scene.eevee.taa_render_samples`, Cycles `samples`) — NOT sphere polys. Tune
  those two for the speed/quality trade-off and keep the balls smooth for free.
- **Translucent overlay markers** (e.g. "candidate sites"): give them a sentinel
  element, copy `Oxygen_ball.scale` to match O size, set the Principled BSDF
  `Alpha < 1`, and `mat.blend_method='BLEND'` (+ `surface_render_method='BLENDED'`
  on EEVEE Next). Render with `film_transparent=True`.


## 화학식 라벨 아래 첨자 (2026-10-04 사용자 지시)
그림 안의 화학식은 숫자를 항상 아래 첨자로 쓴다. "Pd17Pt38O22"를 그대로 찍지 않는다.
- matplotlib: `Pd$_{17}$Pt$_{38}$O$_{22}$` (PdPt 프로젝트는 `formula_pil.formula_tex()`).
- PIL 몽타주와 GIF: `03_paper_prep/scripts/formula_pil.draw_formula(draw, xy, s, font, sub_font)`. E_a 같은 기호도 아래 첨자로 그린다.
- 그림을 저장한 뒤 라벨 영역을 잘라 직접 보고 확인한다.
