# Stitching the 5 parts of a VR180 video using ffmpeg

Note that this is the method used in ``postprocessing.combine_five_parts()``.

You can use the following command to stitch the 5 parts of a VR180 video:

``ffmpeg -i FRONT.mp4 -i TOP.mp4 -i BOTTOM.mp4 -i LEFT.mp4 -i RIGHT.mp4 -filter_complex 'movie="masks/vr180mask_front.png"[FrontMaskIn];[FrontMaskIn][0]scale2ref[FrontMaskScaled][Front];[FrontMaskScaled]format=pix_fmts=yuva444p,alphaextract[FrontMask];movie="masks/vr180mask_t_small.png"[TopMaskIn];[TopMaskIn][1]scale2ref[TopMaskScaled][Top];[TopMaskScaled]format=pix_fmts=yuva444p,alphaextract[TopMask];movie="masks/vr180mask_b_small.png"[BottomMaskIn];[BottomMaskIn][2]scale2ref[BottomMaskScaled][Bottom];[BottomMaskScaled]format=pix_fmts=yuva444p,alphaextract[BottomMask];movie="masks/vr180mask_left.png"[LeftMaskIn];[LeftMaskIn][3]scale2ref[LeftMaskScaled][Left];[LeftMaskScaled]format=pix_fmts=yuva444p,alphaextract[LeftMask];[Front][FrontMask]alphamerge[FrontOut];[Top][TopMask]alphamerge[TopOut];[Bottom][BottomMask]alphamerge[BottomOut];[Left][LeftMask]alphamerge[LeftOut];[4][LeftOut]overlay=shortest=1[RL];[RL][BottomOut]overlay=shortest=1[RLB];[RLB][TopOut]overlay=shortest=1[RLBT];[RLBT][FrontOut]overlay=shortest=1[out]' -i AUDIO.mp3 -map 5:a -map [out]:v OUTPUT.mp4'``

...where ``FRONT.mp4``, ``TOP.mp4``, ``BOTTOM.mp4``, ``LEFT.mp4``, and ``RIGHT.mp4`` are the 5 parts; ``AUDIO.mp3`` is the audio file (if no audio is desired, omit ``-i AUDIO.mp3 -map 5:a`` at the end); ``OUTPUT.mp4`` is the path to the output file; and the working directory contains a subdirectory ``masks``, which contains the same PNG masks as what's in this repo.

The output will be as long as the longest input, including the audio. For some reason, ffmpeg's ``-vframes`` and ``-frames`` options don't work for this command (probably a ffmpeg bug), so either trim the inputs first or trim the output when it's done, if needed.
