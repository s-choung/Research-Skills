---
name: rxn-diagram-inset
description: Use when drawing a reaction energy diagram with Blender-rendered structure insets next to each state (원형 fade 인셋, 다이어그램에 구조 그림, energy diagram with structures, integrated figure with renders, 인셋 다이어그램). Child skill of matplotlib-scientific / rxn-diagram.
---

# Reaction Diagram with Blender Structure Insets

Level-line free-energy diagram where each state carries a circular-fade inset
cropped from a Blender top-view render (no-box, transparent background), plus
plain gas-phase molecule renders at the reactant/product ends.

**REQUIRED BACKGROUND:** matplotlib-scientific rules apply (Arial
FontProperties, no grid, no tight_layout, audit text overlap). rxn-diagram
conventions apply for levels/connectors/labels.

## Core pattern

```python
import sys
sys.path.insert(0, '/Users/sean/.claude/skills/matplotlib-scientific/rxn-diagram-inset')
from mol_inset import mol_circle, add_inset

img = mol_circle(f"{R}/state_nobox_top.png", ox=-140, oy=30)   # surface state
gas = mol_circle(f"{R}/gas_products_fs.png", gasmode=True)     # gas: NO fade
add_inset(ax, img, x, iy, zoom=0.36)
```

Full working exemplar: `example_fig1_integrated.py` (Fig 1, CeO2 ketonization
3-B path: 9 states, per-state table with label side, inset dx/dy, per-system
center tweaks, largest-step highlight).

## Layout recipe (what made Fig 1 work)

- Per-state table: `(key, label, side, render, gasmode, label_dy,
  inset_dy_extra, inset_dx, (ox, oy), connector_gas_label)`.
- Inset goes on the SAME side as the state label, stacked beyond it:
  `iy = y +/- (8 + label_dy + INSET_KJ + inset_dy_extra + (nlines-1)*16)`,
  INSET_KJ ~ 72 (in y-data units). Keep insets CLOSE to their label --
  user rejects big vertical gaps.
- Crop half-size 460 px on 1600 px renders, out 400 px, zoom ~ 0.36.
  Two co-adsorbed fragments (PBC split): widen to ~500-560 px.
- Widen ylim (~+/-30%) to make room; `subplots_adjust`, not tight_layout.

## Hard-won rules

1. **Carbon centering is manual.** Dark-pixel median lands mid-frame (surface
   shadow crevices dominate). Always render -> Read the PNG -> set per-system
   `(ox, oy)` in render px -> repeat (1-2 rounds).
2. **Gas renders never get the fade** -- plain alpha-bbox crop.
3. **Crop must stay inside the render frame** or the circle shows a flat
   clipped edge; shrink |oy|/size rather than accept padding.
4. Stagger neighboring insets (dx shift +/- up to 0.3 x-units, dy) so circles
   don't collide and don't cover the next state's label; e.g. move an inset
   left+up when its neighbor's label crowds it.
5. Labels: no over-compressed formulas -- write out species with line breaks
   ("CO$_2$* + CH$_2$C(CH$_3$)O*\n+ 2 H*"), keep off the connectors.
6. Save PNG (dpi ~ 220); AnnotationBbox images do not survive SVG text-editing
   workflows well.

## Blender render inputs

Renders come from `blender --background --python render_autoframe_v2.py --
in.xyz out.png top ... cz` with `cz=-1` (no box, atom framing) -> 1600x1600
RGBA `*_nobox_top.png`. Gas molecules: standalone `gas_*_fs.png` renders.
