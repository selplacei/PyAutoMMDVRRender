# Rendering high-quality/lossless videos on Linux

As you may know, the only two codecs available to Linux MMD users are MJPEG and AVI Raw. No matter how hard you try, all other codecs will crash or give you an error.

MJPEG certainly can work if you're fine with it, but it messes up colors noticeably. I want my videos to look nicer, so I went the AVI Raw route.

### Converting to mp4

Due to the huge size of raw video files, it makes sense to compress them to mp4 before doing anything else with them. You can do this using `ffmpeg -i input.avi -vcodec libx264 output.mp4 && rm input.avi`, or by using convert_split() in PyAutoMMDVRRender's config (which is the case in the default config).

### Splitting output to save space

Even a few seconds of raw video can take up gigabytes of storage. PyAutoMMDVRRender has functionality for automatically splitting the output into several chunks; just set the SPLIT variable in `config.py` and implement `after_split()` and `merge_split()` (once again, the default config should do the job).

To figure out how big the splits should be (for your system and project configuration), you can render 100 frames of video, then divide your available storage space by the size of that output file and then by 100. Round this to an integer, and use the result as the value for SPLIT.

### Speeding up rendering by eliminating the I/O bottleneck

Since the amount of data written to the disk is so huge, disk I/O can end up being the main bottleneck for rendering speed. It can also deteriorate the disk health if you render videos all the time. If you see that the first ~100 frames of your videos render really fast and then it slows down, disk I/O is likely your main bottleneck.

To solve this, you can write the AVI files to RAM using tmpfs, and then just save the final stitched output to the hard drive. You can set this up as follows:

1. Figure out how much RAM will be available (leave some room for running programs). You can set up swap if you haven't already to make sure that you don't accidentally run out of space.
2. Create a tmpfs of that size. Don't use /tmp (or other default directories) unless you're sure they have enough space allocated.
3. Set up the SPLIT variable so that a single split can fit into the tmpfs.
4. Adjust `after_split()`, `merge_splits()`, and `post_process()` so that the AVI files are deleted immediately after being re-encoded and so that the final output is saved to a permanent location. If you're using the default configuration, all you have to do is set OUTPUT inside the tmpfs and FINAL_OUTPUT to a permanent location.

### Rendering while using the PC normally

Unless you want to render overnight, which wastes electricity, makes your room warmer, and only allows one render per day (come on, you don't stamp out mediocre content like a factory?), it is useful to render MMD videos while being able to use the PC as normal. We can do this using a dummy X11 display with its own keyboard and mouse input. Good luck doing that on Windows.

Choose a window manager - I use KWin normally, so that's also what I will use here. The window manager should be compatible with `wmctrl` and allow MMD windows to set their own geometry. In other words, when you launch MMD, its windows should have the same size and position as when you exited it. This wasn't the case with OpenBox but YMMV.

1. Install `Xvfb`. On Arch Linux, this is in the `xorg-server-xvfb` package, which should already be installed if you have Xorg.
   Optionally, also install `x11vnc` and `tigervnc` (provides the `vncviewer` command) to be able to view what's happening.
2. Use the following script (saved as `render.sh` in this repo):

    ```
    #!/usr/bin/env sh
	export DISPLAY=":1"
	Xvfb :1 -screen 0 1920x1080x24 &
	kwin_x11 &
	if [[ $1 == "--vnc" ]]; then
		x11vnc -display :1 -bg -nopw -listen localhost -xkb &
		DISPLAY=:0 vncviewer localhost:5900 &
	fi
	python PyAutoMMDVRRender/main.py --start
	killall Xvfb
	```
	
  Adjust this script according to your configuration, specifically:
  - The screen resolution should be the same as the monitor MMD normally launches on.
    MMD will remember its precise geometry, so you don't have to subtract taskbars and such from the screen resolution.
    The third value is the bit depth, keeping it at 24 should be fine.
  - Change `kwin_x11` to your WM of choice if needed.
  - Adjust the path to `main.py`.
3. If you passed `--vnc` to the script, it will launch TigerVNC, which shows the virtual display.
   In my experience, messing with the TigerVNC window (such as moving it to a different virtual desktop) breaks the automation.
   To be safe, just open it, stare at it to see if PyAutoMMDVRRender works fine, then close it. You can always open it again by running `vncviewer localhost:5900`.

