# Workaround for visible stitches between the angles of a VR video

**Note: this is about MME effects, not model physics.**

When using certain effects, such as AutoLuminous or RayMMD's fog, there can be a visible boundary between the 6 parts of a VR video made with EquirectangularX. For example:

![Areas surrounding light sources appear in noticeably different colors, with a sudden change between the front, left, right, and bottom parts.](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_1.jpg?raw=true)

This happens due to how effects react to the camera angle and whether something is visible on the screen at the time of rendering. All effects work in different ways, so rather than trying to solve this issue for every effect you ever use, you can use post-processing to somewhat hide the transition. This is the end result for the example video - it's not perfect, but it's much better:

![It's mostly smooth.](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_2.jpg?raw=true)

## Basic idea

We start off with 6 parts: top, bottom, front, left, and right. Each of these represents a rotation of the camera by 90 degrees in some direction. This is the normal way to make VR MMD videos.

We will render two additional parts: one for a -45 degree rotation about the Y axis, and one for 45. Let's call them "half-left" and "half-right". This will give us something like this, overall:

![Something like the left, front, and right parts combined, but shaped like two front parts put side by side.](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_3.jpg?raw=true)

We will then apply a mask with a gradient of transparency, so that only the half-left pixels can be seen where the normal left part meets the front, only left pixels can be seen on the left edge, and only front pixels can be seen in the middle (vice versa for the right parts). With the mask applied, half-left and half-right parts on a black background look like this:

![The left edge, a vertical line in the middle, and the right edge are black; between them, there is a gradual transition into the half-left and half-right parts.](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_4.jpg?raw=true)

## Method

People have different methods for putting the 6 parts of a VR video together. Some use a chroma key on black (EquirectangularX also allows you to make the background green, which is even better), but I find that this is inconsistent and hard to use. Instead, I use masking: by applying one of the images in [the masks folder in this repo](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/masks), I always get the same result with the same shape.

The following can be done in any reasonable video editing software - I will use Kdenlive as an example because I'm used to it and because it's free.

Loading many clips and tracks into a single project makes my PC suffer, so I will first put together just the top, front, and bottom parts. First, import the clips:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_5.jpg?raw=true)
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_6.jpg?raw=true)

Add two video tracks, for a total of three:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_7.jpg?raw=true)

Put FRONT at the top, TOP below it, and BOTTOM below that:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_8.jpg?raw=true)

Add the "Shape Alpha (Mask)" effect to FRONT:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_9.jpg?raw=true)
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_10.jpg?raw=true)
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_11.jpg?raw=true)

Load the `vr180mask_front.png` mask:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_12.jpg?raw=true)
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_13.jpg?raw=true)

Do the same for TOP with the `vr180mask_top_big.png` mask:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_14.jpg?raw=true)

Since BOTTOM is the first layer, you don't have to do anything to it.

Render the video - let's call it "TFB" (for Top, Front, Bottom):
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_15.jpg?raw=true)

Now, start a new Kdenlive project. This is the one where magic happens.

Import TFB, HALFLEFT, HALFRIGHT, LEFT, and RIGHT:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_16.jpg?raw=true)

Add 4 new video tracks for a total of five:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_17.jpg?raw=true)

Place the clips in the following order:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_18.jpg?raw=true)

Apply the masks `vr180mask_halfleft_gradient.png` and `vr180mask_halfright_gradient` to HALFLEFT and HALFRIGHT, respectively. Make sure that the three checkboxes on the right (Invert, Use Luma, Use Threshold) are unchecked (on both HALFLEFT and HALFRIGHT):
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_19.jpg?raw=true)

We still haven't applied a mask to TFB, so you can't see the left and right parts properly. Now, since we're blurring and smoothing edges anyway, let's also smooth the transition to BOTTOM and TOP by using the `vr180mask_tfb_smaller_gradient.png` (rather than the one without a gradient):
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_20.jpg?raw=true)

Once again, make sure the 3 checkboxes on the right are unchecked.

Finally, make the RIGHT part visible by applying the `vr180mask_left.png` to LEFT:
![Screenshot](https://github.com/selplacei/PyAutoMMDVRRender/blob/main/HowTo/img/2_21.jpg?raw=true)

Add audio if necessary and now it should be ready to render. As a tip, if Kdenlive takes up a lot of RAM, you can press "Generate script" instead of "Render to file", save it, restart Kdenlive, press "Render" without loading a project, go to the "Scripts" tab, and render the script that was just created.
