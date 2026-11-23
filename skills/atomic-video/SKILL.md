---
name: atomic-video
description: Guideline for making atom-scale reaction videos (mp4) with a coding agent. A reaction pathway is constructed on surface sites or steered in a short MD, then rendered with Blender Cycles. Triggers - reaction video, catalyst animation, atomic video, constructed pathway, pathway video, 반응 영상, 촉매 영상, 원자 애니메이션.
---

# atomic-video: reaction videos from a constructed pathway

A general guideline in two parts: generating the pathway, and rendering it with Blender Cycles.
It describes the method only. Write the scripts for your own system with a coding agent.

> **Disclaimer.** The pathway is constructed or steered (steered MD) for explanation. It may not reflect the actual physical process, and it carries no energetics or kinetics. Say so wherever the video is shown.

Examples made this way: dry reforming of methane on NiMo/MgO, Fischer-Tropsch chain growth on Co/CeO2, Rh-catalysed hydroformylation in toluene, and CO2 electroreduction on Cu(111).

## Part 1. Pathway generation

The goal is a video in which a viewer reads "reactants arrive, split on the surface, and products leave" at a glance.
Waiting for a reaction in plain MD rarely gives that, so the motion is written as keyframes.

### Steps

1. **Start structure.** One structure file of support plus particle (or slab, or complex). Check that the particle touches the support: print the shortest metal-support distance and the number of contact atoms.
2. **Thermal vibration (optional).** A short MD of the support and particle with an MLIP, about 100 frames, played back and forth as a loop. Reacting atoms are not in this MD.
3. **Sites.** Find top sites and three-fold hollows on the exposed surface and build a neighbour graph. Fix an adsorption height per element.
4. **One reaction cycle as keyframes.** For each atom write (frame, position, motion type). Four motion types are enough: smooth move, arc hop between sites, decelerating straight flight in, accelerating straight flight out.
5. **Many cycles.** Overlap cycles in time and record site occupancy per time window, so two cycles never use the same site.
6. **Interpolate** keyframes to every frame, and let adsorbed atoms follow the vibration of the metal atoms below them.
7. **Check by numbers** before rendering anything.

### Motion rules

- Gas molecules arrive and leave on nearly straight lines. They do not stop in mid-air and do not arrive all at once.
- Fragments diffuse by hops before they meet and react. They do not bond where they were formed.
- Site choice, timing and hop count are randomised. Periodic repetition looks artificial.
- Choose flight directions that pass no other atom closely.
- Products can be recoloured from the frame in which they form.

### Numeric checks

| Item | What to look for |
|---|---|
| shortest distance between reacting atoms | not below the shortest real bond (H-H) |
| shortest distance to a metal atom | atoms do not sink into the particle |
| products per cycle | matches the stoichiometry |
| sites used, reacting atoms per frame | the frame is not empty and events are spread out |
| frame-to-frame scan | no teleports, no sudden bond-length changes, no unintended spins |

### Molecular catalysts and liquids

- With no surface there is no site lattice. Run a short MD and move distance restraints to pull the system through each step (steered MD), then attach straight flights for molecules before they enter and after they leave.
- Build the vacuum version first and add solvent afterwards.
- Solvent can be constructed motion as well: molecules on a lattice at liquid density with random offsets, slow drift per molecule, drawn nearly transparent, and pushed aside when a reacting molecule passes.

## Part 2. Blender Cycles

1. **Preview first.** Check the pathway in a light viewer (a single html file or a fast ray tracer) and agree on the camera angle before any Cycles render.
2. **One scene per frame.** A Python script (bpy) reads the per-frame coordinates, places one sphere per atom with a material per element, sets the camera and lights, and renders one image. Draw every atom.
3. **Transparent background** if the video will be composited on a page.
4. **Time ten frames**, multiply, and state the estimate before the full run.
5. **Run several Blender processes in parallel** on one GPU, each on its own frame range.
6. **Encode** the frames with ffmpeg and decode the result to the end once (`ffmpeg -v error -i out.mp4 -f null -`) before sharing it.

### Measured time and cost

| Step | Condition | Time | Machine |
|---|---|---|---|
| pathway generation | about 2,000 frames, 1,500 to 2,300 atoms | tens of seconds | laptop CPU |
| Blender Cycles | Rh complex in toluene, 720x720, 278 frames | 2.8 s per frame, about 13 min | one cloud GPU (NVIDIA A40), about 0.22 USD |

In the Cycles run the per-frame scene build in Python was the limit, not the GPU, so a mid-range card is enough.

Requirements: Python with `numpy` and `ase`, Blender, ffmpeg. An MLIP calculator is needed only for the vibration loop and the steered MD.
