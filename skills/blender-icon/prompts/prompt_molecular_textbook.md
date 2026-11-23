# Molecular Textbook

Use the blender-icon skill (github.com/s-choung/Research-Skills/tree/master/skills/blender-icon).

Make a 3D icon with a looping motion for my web page.
Icon: An open book tilted toward the viewer, with a navy cover and white pages with gray text lines, and an ethanol molecule above it.
Motion: The book starts closed, both covers open about the spine, ethanol rises from the middle, and three gold rays extend toward it.

Build it from primitive shapes in Blender (bpy): rounded boxes, spheres, cylinders and tori, about 15 parts.
Write the motion as one Python function of a phase t in [0, 1], with no keyframes. The last frame is the resting pose.
Render with Cycles on a transparent background and keep only a soft floor shadow.
Render a 12-frame low-resolution preview first and show me every frame on one sheet.
After I approve, render 24 frames and pack them into one sprite strip.

Source: schoung.com/resource/blender_icon
