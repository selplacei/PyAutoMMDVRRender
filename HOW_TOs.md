# Rendering high-quality/lossless videos on Linux

As you may know, the only two codecs available to Linux MMD users are MJPEG and AVI Raw. No matter how hard you try, all other codecs will crash or give you an error.

MJPEG certainly can work if you're fine with it, but it messes up colors noticeably. I want my videos to look nicer, so I went the AVI Raw route.

### Converting to mp4

Due to the huge size of raw video files, it makes sense to compress them to mp4 before doing anything else with them. You can do this using `ffmpeg -i input.avi -vcodec libx264 output.mp4 && rm input.avi`.

### Splitting output to save space

Even a few seconds of raw video can take up gigabytes of storage. PyAutoMMDVRRender has functionality for automatically splitting the output into several chunks; just set the SPLIT variable in `config.py` and implement `after_split()` and `merge_split()` (working examples are provided in the repo).

To figure out how big the splits should be (for your system and project configuration), you can render 100 frames of video, then divide your available storage space by the size of that output file and then by 100. Round this to an integer, and use the result as the value for SPLIT.

### Speeding up rendering by eliminating the I/O bottleneck

Since the amount of data written to the disk is so huge, disk I/O can end up being the main bottleneck for rendering speed. It can also deteriorate the disk health if you render videos all the time. If you see that the first ~100 frames of your videos render really fast and then it slows down, disk I/O is likely your main bottleneck.

To solve this, you can write the AVI files to RAM using tmpfs, and then just save the final stitched output to the hard drive. You can set this up as follows:

1. Figure out how much RAM will be available (leave some room for running programs). You can set up swap if you haven't already to make sure that you don't accidentally run out of space.
2. Create a tmpfs of that size. Don't use /tmp (or other default directories) unless you're sure they have enough space allocated.
3. Set up the SPLIT variable so that a single split can fit into the tmpfs.
4. Adjust `after_split()`, `merge_splits()`, and `post_process()` so that the AVI files are deleted immediately after being re-encoded and so that the final output is saved to a permanent location. The default configuration should do just fine as long as you adjust the final output path in `post_process()`.
