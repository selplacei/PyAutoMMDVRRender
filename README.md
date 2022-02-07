# PyAutoMMDVRRender

This script is meant to be run on a Linux system that uses Wine to run MMD.

One way to make spherical/VR videos in MMD is to use the EquirectangularX filter.
Since it requires rendering at least 8, usually 10, separate AVIs, it makes sense to automate this.

## How to use it

Open a terminal and run `main.py` using Python. It'll give you a basic overview of what to do. 
Make sure to adjust the config file according to your system and project configuration.

Additionally, if you need to render a different set of AVIs (such as a 360 video), adjust the
`PARTS` value in `main.py`. The arguments to `Part()` are in the following order:

- Filename suffix
- Camera X offset
- Camera X rotation
- Camera Y rotation
- Value of Ry for EquirectangularX.x

This script will work even if you have multiple camera keyframes -
just make sure that all of them have X and Y rotation angles between -90 and 90.

## License

See the `LICENSE` file (TL;DR: Apache 2.0).
