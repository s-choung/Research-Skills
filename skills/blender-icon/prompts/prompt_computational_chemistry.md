# Computational Chemistry

Use the blender-icon skill (github.com/s-choung/Research-Skills/tree/master/skills/blender-icon).

Make a 3D icon with a looping motion for my web page.
Icon: An open silver laptop with a navy screen and an ethanol molecule above it.
Motion: The laptop and the molecule turn once about the vertical axis.

Build it from primitive shapes in Blender (bpy): rounded boxes, spheres, cylinders and tori, about 15 parts.
Write the motion as one Python function of a phase t in [0, 1], with no keyframes. The last frame is the resting pose.
Render with Cycles on a transparent background and keep only a soft floor shadow.
Render a 12-frame low-resolution preview first and show me every frame on one sheet.
After I approve, render 24 frames and pack them into one sprite strip.

Source: schoung.com/resource/blender_icon
