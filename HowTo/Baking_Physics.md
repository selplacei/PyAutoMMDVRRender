# Baking physics

If you've been following VR MMD tutorials, the most popular one mentions using MikuMikuMoving to "bake" the physics - that is, calculate all positions for physical bones and put them into a motion so that new calculations don't have to be done every time a video is rendered.

I haven't been able to get MMM working on Linux - even in a virtual machine, as it requires DirectX, and I don't have a second GPU for doing passthrough. Instead, there is a way to bake physics using PMXE, which does work on Linux (see the other HowTo on how to set it up).

## Process

- Open PMXE and load the desired model.
- In PMXView, click Info, VMD View, and Slave Mode.
- Click File, Open VMD (Individual), and Model Motion. Find the desired VMD file.
- Click Edit, then Motion-Fix.
- When it's done, click File, then Save Fix-Motion. Choose the desired location (don't overwrite the original file).

## Main drawback

Unlike MMM, there is no way to specify the keyframe rate per second, nor to export only a specific set of bones into the motion. This means that you may exceed MMD's limit of 600,000 keyframes per project, preventing you from importing the motion; this is especially likely to happen with models that have a lot of physical bones.

There are at least three ways to work around this:

- Use PMXE itself to delete all but one set of physical bones; do this for all sets of bones, resulting in several VMD files that could be imported one-by-one (adjusting them in MMD as needed).
- Use MMD to split the motion into several chunks (e.g. first and second half of the motion), then bake them separately. Again, this may give you the ability to adjust each chunk before importing the next one.
- Vaguely follow [this guide](https://www.deviantart.com/hanaki-han/art/How-to-load-motions-with-frame-limit-in-MMD-720369010); there's no need for MMM though, as you can just load the original motion into MMD, select facial keyframes etc., and save the motion data. You can also do this to the "filtered" motion to only keep its physical bone keyframes while preserving other keyframes from the original.
- Give up and use MMM on a dual-boot OS or a dedicated computer. This is the unfortunate truth - as long as there hasn't been found a way to make MMM work in Wine, this is the easiest option if you have the ability to do it. I only resort to this if absolutely needed.
