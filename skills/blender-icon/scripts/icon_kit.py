# blender-icon kit: clay-style 3D icons and their motions, built from primitive shapes in Blender (bpy).
#
# Usage
#   blender -b -P icon_kit.py -- <out_dir> [size_px]
# Environment
#   ONLY=name1,name2   render only these icons
#   FRAMES=24          render a 24-frame motion (name_f00.png ...) instead of one still (name.png)
#   SAMPLES=48         Cycles samples (default 96)
#   THREADS=6          CPU threads
#   SKIP=1             keep frames that already exist (resume)
#
# One icon is one Python function. A motion icon takes a phase t in [0, 1] and rebuilds the whole scene at that
# phase, so no Blender keyframes are used. t = 1 is the resting pose and doubles as the still icon.
# A spin icon takes no argument and is rendered while the whole group turns once.
import bpy, sys, os, math, time, traceback
from mathutils import Vector, Matrix, Euler

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]
RES = int(argv[1]) if len(argv) > 1 else 512
os.makedirs(OUT, exist_ok=True)

NAVY, GREEN, LIME, ORANGE = "#072B61", "#124633", "#8DC63F", "#FF6C0F"
WHITE, GRAY, DARK, GOLD, RED, BLUE, SILVER = "#FBF8F1", "#C3C9D2", "#24292F", "#F2B632", "#E5533D", "#3B82F6", "#D5D8DD"
_mats = {}


# ---------------- materials ----------------
def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def M(hexcol, rough=0.55):
    """Cached Principled material from a hex colour."""
    k = (hexcol, rough)
    if k not in _mats or _mats[k].name not in bpy.data.materials:
        h = hexcol.lstrip("#")
        m = bpy.data.materials.new("m" + hexcol)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*[_lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)], 1)
        b.inputs["Roughness"].default_value = rough
        _mats[k] = m
    return _mats[k]


# ---------------- primitives ----------------
def _smooth(o, angle=40):
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    for p in o.data.polygons:
        p.use_smooth = True
    if hasattr(o.data, "use_auto_smooth"):                 # Blender < 4.1
        o.data.use_auto_smooth = True
        o.data.auto_smooth_angle = math.radians(angle)
    else:
        try:
            bpy.ops.object.shade_smooth_by_angle(angle=math.radians(angle))
        except Exception:
            try:
                bpy.ops.object.shade_auto_smooth(angle=math.radians(angle))
            except Exception as e:
                print("auto smooth skipped:", e)


def rbox(size, bev, m, loc=(0, 0, 0), rot=(0, 0, 0)):
    """Box with bevelled edges. Every box should go through this, the round edges give the clay look."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    md = o.modifiers.new("Bevel", "BEVEL")
    md.width, md.segments, md.limit_method = bev, 6, 'ANGLE'
    _smooth(o)
    o.data.materials.append(m)
    return o


def sph(r, m, loc=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=48, ring_count=24, location=loc)
    o = bpy.context.active_object
    o.scale = scale
    for p in o.data.polygons:
        p.use_smooth = True
    o.data.materials.append(m)
    return o


def cyl(r, depth, m, loc=(0, 0, 0), rot=(0, 0, 0), r2=None, verts=96):
    """Cylinder, or a cone frustum when r2 (top radius) is given."""
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=depth, vertices=verts, location=loc, rotation=rot)
    o = bpy.context.active_object
    _smooth(o)
    o.data.materials.append(m)
    return o


def cyl_between(p1, p2, r, m, r2=None):
    """Rod from p1 to p2 (a cone when r2 is given). Bonds, arms, wires."""
    p1, p2 = Vector(p1), Vector(p2)
    v = p2 - p1
    o = cyl(r, v.length, m, loc=(p1 + p2) / 2, r2=r2, verts=24)
    o.rotation_euler = v.to_track_quat('Z', 'Y').to_euler()
    return o


def torus(R, r, m, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=96, minor_segments=20,
                                     location=loc, rotation=rot)
    o = bpy.context.active_object
    o.scale = scale
    for p in o.data.polygons:
        p.use_smooth = True
    o.data.materials.append(m)
    return o


def prism(pts, y0, y1, m):
    """Extrude a polygon given as (x, z) points from depth y0 to y1. Energy profiles, arrows, roofs."""
    n = len(pts)
    verts = [(x, y0, z) for x, z in pts] + [(x, y1, z) for x, z in pts]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    me = bpy.data.meshes.new("prism")
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new("prism", me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(m)
    return o


# ---------------- molecules ----------------
# element: (colour, ball radius). Coordinates in angstrom: (element, x, y, z), then bonds as index pairs.
ELEMENTS = {"C": ("#3A3D42", 0.2), "O": ("#E5533D", 0.19), "H": ("#FBF8F1", 0.12), "N": ("#3B82F6", 0.19)}
WATER = ([("O", 0, 0, 0), ("H", 0.76, 0.59, 0), ("H", -0.76, 0.59, 0)], [(0, 1), (0, 2)])
METHANOL = ([("C", 0, 0, 0), ("O", 1.43, 0, 0), ("H", -0.36, 1.03, 0), ("H", -0.36, -0.51, 0.89), ("H", -0.36, -0.51, -0.89),
             ("H", 1.75, 0.75, 0.5)], [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5)])
ETHANOL = ([("C", 0, 0, 0), ("C", 1.52, 0, 0), ("O", 2.0, 1.35, 0), ("H", 2.95, 1.3, 0), ("H", -0.36, 1.03, 0),
            ("H", -0.36, -0.51, 0.89), ("H", -0.36, -0.51, -0.89), ("H", 1.88, -0.51, 0.89), ("H", 1.88, -0.51, -0.89)],
           [(0, 1), (1, 2), (2, 3), (0, 4), (0, 5), (0, 6), (1, 7), (1, 8)])


def molecule(spec, centre, s, tilt=0.0):
    """Ball-and-stick molecule. Molecular x, y, z map to scene x, z (up), y (depth); tilt rotates in the x-z plane."""
    atoms, bonds = spec
    mx = sum(a[1] for a in atoms) / len(atoms)
    my = sum(a[2] for a in atoms) / len(atoms)
    ct, st = math.cos(tilt), math.sin(tilt)
    pos = []
    for _, x, y, z in atoms:
        x, y = x - mx, y - my
        pos.append((centre[0] + s * (x * ct - y * st), centre[1] + s * z, centre[2] + s * (x * st + y * ct)))
    ps = [cyl_between(pos[i], pos[j], 0.11 * s, M(GRAY)) for i, j in bonds]
    for (el, *_), p in zip(atoms, pos):
        ps.append(sph(ELEMENTS[el][1] * s * 2.1, M(ELEMENTS[el][0], 0.4), p))
    return ps


# ---------------- motion helpers ----------------
def seg(t, a, b):
    """0 -> 1 while t goes from a to b. Give every part its own time window."""
    return max(0.0, min(1.0, (t - a) / (b - a)))


def ease(x):
    return x * x * (3 - 2 * x)


def back(x):
    """0 -> 1 with a small overshoot, for parts that pop in."""
    c = 1.70158
    x -= 1
    return 1 + (c + 1) * x ** 3 + c * x ** 2


def lerp(a, b, k):
    return tuple(x + (y - x) * k for x, y in zip(a, b))


def xf(parts, s=1.0, pivot=(0, 0, 0), loc=(0, 0, 0), rot=(0, 0, 0)):
    """Scale and rotate finished parts about a pivot, then shift them. Hinges: lids, fingers, book covers."""
    bpy.context.view_layer.update()
    P = Matrix.Translation(pivot)
    T = Matrix.Translation(loc) @ P @ Euler(rot).to_matrix().to_4x4() @ Matrix.Scale(s, 4) @ P.inverted()
    for p in parts:
        p.matrix_world = T @ p.matrix_world
    return parts


def pop(build, k, pivot, drop=0.0):
    """Parts from build() popping in with progress k; nothing while k is 0. drop: start height above the final place."""
    if k <= 0:
        return []
    return xf(build(), s=max(0.03, back(k)), pivot=pivot, loc=(0, 0, drop * (1 - ease(k))))


def star(c, r, col=GOLD):
    """Sparkle. Multiply r by math.sin(math.pi * seg(...)) to make it appear and vanish."""
    m = M(col, 0.3)
    return [sph(r, m, c), rbox((r * 3.4, r * 0.5, r * 0.5), r * 0.2, m, loc=c), rbox((r * 0.5, r * 0.5, r * 3.4), r * 0.2, m, loc=c)]


# ---------------- scene ----------------
def reset_scene():
    """Empty scene, orthographic camera, two suns, transparent film, shadow-catcher floor."""
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    _mats.clear()
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = int(os.environ.get("SAMPLES", "96"))
    try:
        sc.cycles.use_denoising = True
    except Exception:
        pass
    if os.environ.get("THREADS"):
        sc.render.threads_mode = 'FIXED'
        sc.render.threads = int(os.environ["THREADS"])
    sc.render.resolution_x = sc.render.resolution_y = RES
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'
    w = sc.world or bpy.data.worlds.new("W")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (1, 1, 1, 1)
    bg.inputs[1].default_value = 0.55
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    bpy.context.active_object.is_shadow_catcher = True
    cd = bpy.data.cameras.new("cam")
    cd.type = 'ORTHO'
    cd.ortho_scale = 4.1
    cam = bpy.data.objects.new("cam", cd)
    bpy.context.collection.objects.link(cam)
    target = Vector((0, 0, 0.8))
    cam.location = target + Vector((0, -1, 0.42)).normalized() * 12
    cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = cam
    for nm, e, ang, d in [("key", 2.6, 25, (-0.22, -0.3, -1)), ("fill", 0.6, 60, (0.8, -0.5, -0.4))]:
        ld = bpy.data.lights.new(nm, 'SUN')
        ld.energy = e
        ld.angle = math.radians(ang)
        lo = bpy.data.objects.new(nm, ld)
        bpy.context.collection.objects.link(lo)
        lo.rotation_euler = Vector(d).to_track_quat('-Z', 'Y').to_euler()


def place(parts, yaw=-22, pitch=-5, s=1.0):
    """Parent all parts to one empty and turn the whole icon toward the camera."""
    e = bpy.data.objects.new("grp", None)
    bpy.context.collection.objects.link(e)
    for p in parts:
        if p.parent is None:
            p.parent = e
    e.location = (0, 0, 0.02)
    e.rotation_euler = (math.radians(pitch), 0, math.radians(yaw))
    e.scale = (s,) * 3
    return e


def render(name):
    bpy.context.scene.render.filepath = os.path.join(OUT, name + ".png")
    bpy.ops.render.render(write_still=True)


# ---------------- example icons ----------------
# Build inside x -1..1, z 0..2 (x right, z up, -y toward the camera). Scale down in ICONS if it overflows.
def a_hand(t):
    """Atomic hand: a fist opens and a methanol molecule pops up above the palm."""
    skin = "#F0C8A0"
    c = 1 - ease(seg(t, 0.08, 0.5))                                 # 1 = fist, 0 = open
    hand = [rbox((1.05, 1.0, 0.26), 0.11, M(skin), loc=(0, 0.15, 0)), rbox((0.8, 0.5, 0.34), 0.1, M(NAVY), loc=(0, 0.85, 0))]
    for x, ln in [(-0.39, 0.62), (-0.13, 0.76), (0.13, 0.7), (0.39, 0.52)]:
        f = [rbox((0.21, ln, 0.21), 0.09, M(skin), loc=(x, -0.3 - ln / 2, 0.06), rot=(math.radians(-12), 0, 0))]
        hand += xf(f, pivot=(x, -0.3, 0.1), rot=(math.radians(-158 * c), 0, 0))
    th = [rbox((0.24, 0.6, 0.22), 0.09, M(skin), loc=(-0.72, -0.1, 0.05), rot=(0, 0, math.radians(-32)))]
    hand += xf(th, pivot=(-0.55, -0.1, 0.1), rot=(0, math.radians(115 * c), 0))
    xf(hand, rot=(math.radians(14), 0, math.radians(-12)), loc=(0, 0, 0.5))
    k = seg(t, 0.5, 0.88)
    m = (0.0, -0.1, 1.5)
    if k > 0:
        hand += xf(molecule(METHANOL, m, 0.42, tilt=math.radians(12)), s=max(0.03, back(k)), pivot=m, loc=(0, 0, -0.6 * (1 - ease(k))))
    return hand


def p_crystal():
    """Body-centred cubic unit cell: eight corner atoms, one centre atom, twelve edges."""
    a, c0 = 0.65, (0, 0, 0.95)
    cs = [Vector((sx * a, sy * a, c0[2] + sz * a)) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    ps = [sph(0.2, M(NAVY), tuple(c)) for c in cs] + [sph(0.32, M(ORANGE), c0)]
    for i in range(8):
        for j in range(i + 1, 8):
            if sum(1 for k in (cs[i] - cs[j]) if abs(k) > 1e-6) == 1:
                ps.append(cyl_between(tuple(cs[i]), tuple(cs[j]), 0.035, M(GRAY)))
    return ps


def p_laptop():
    """Open laptop with an ethanol molecule above it."""
    tilt = (math.radians(-12), 0, 0)
    ps = [rbox((1.7, 1.15, 0.1), 0.04, M(SILVER, 0.35), loc=(0, 0, 0.08)),
          rbox((1.3, 0.6, 0.02), 0.01, M(DARK), loc=(0, -0.12, 0.14)),
          rbox((1.7, 0.1, 1.15), 0.04, M(SILVER, 0.35), loc=(0, 0.62, 0.68), rot=tilt),
          rbox((1.5, 0.03, 0.95), 0.02, M(NAVY), loc=(0, 0.555, 0.69), rot=tilt)]
    return ps + molecule(ETHANOL, (0, -0.05, 1.75), 0.36, tilt=math.radians(-12))


# name: (function, kind, yaw, scale). kind "motion": function(t). kind "spin": function(), the group turns once.
ICONS = {
    "hand": (a_hand, "motion", -22, 1.0),
    "crystal": (p_crystal, "spin", 28, 1.0),
    "laptop": (p_laptop, "spin", -22, 1.0),
}


# ---------------- run ----------------
def main():
    only = os.environ.get("ONLY")
    frames = int(os.environ.get("FRAMES", "0"))
    for name, (fn, kind, yaw, scale) in ICONS.items():
        if only and name not in only.split(","):
            continue
        t0 = time.time()
        try:
            if not frames:                                          # one still: resting pose
                reset_scene()
                place(fn(1.0) if kind == "motion" else fn(), yaw=yaw, s=scale)
                render(name)
            for k in range(frames):
                tag = "%s_f%02d" % (name, k)
                if os.environ.get("SKIP") and os.path.exists(os.path.join(OUT, tag + ".png")):
                    continue
                reset_scene()
                if kind == "motion":
                    place(fn(k / (frames - 1.0)), yaw=yaw, s=scale)
                else:
                    place(fn(), yaw=yaw + 360.0 * k / frames, s=scale)
                render(tag)
            print("DONE", name, "%.0f s" % (time.time() - t0), flush=True)
        except Exception as e:
            traceback.print_exc()
            print("FAILED", name, e, flush=True)


main()
