# PyAutoMMDVRRender

This script is meant to be run on a Linux system that uses Wine to run MMD.

One way to make spherical/VR videos in MMD is to use the EquirectangularX filter.
Since it requires rendering at least 8, usually 10, separate AVIs, it makes sense to automate this.

This script can be useful for non-VR videos as well: for example, to automate rendering the video
in chunks and converting them to .mp4, and later stitching them together (useful for rendering in AVI Raw).

## How to use it

Make sure that Python 3, PyAutoGUI, and wmctrl are installed. Additionally, the example post-processing functions use ffmpeg.

Open a terminal and run `main.py` using Python. It'll give you a basic overview of what to do. 
Make sure to adjust the config file according to your system and project configuration.

This script will work even if you have multiple camera keyframes (unless you use the viewpoint bone model) -
just make sure that all of them have X and Y rotation angles between -90 and 90.
It will run for a while and you won't be able
to use your PC normally while it's doing its work, so it's a good idea to leave it overnight.

## Tips and tricks

See the `HowTo` directory for useful guides related to this program and using MMD on Linux in general.

## License

See the `LICENSE` file (TL;DR: Apache 2.0).
