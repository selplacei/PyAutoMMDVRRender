"""
Non-VR video example configuration for PyAutoMMDVRRender
This example config will do the following:
- Render the output 500 frames at a time using the AVI Raw codec
- Immediately convert the rendered splits to .mp4
- Automatically put the splits together when they're all rendered
This config will not touch the camera angle, accessory coordinates, etc.
"""
import postprocessing


# Do not edit the following value.
# You can use it instead of any number in any PARTS value to keep the corresponding value
# as what's already in the project, i.e., the script won't change it.
NOCHANGE = []

## Paths and filenames ##
# All paths must be absolute and cannot contain characters that can't be typed on a keyboard
# Path to the .pmm project file
PROJECT = '/mnt/projects/MikuMikuDance/UserFile/project.pmm'
# The base filename of all output videos - don't include the file extension
# If you use the tmpfs trick, this should be inside the tmpfs directory
OUTPUT = '/mnt/projects/MikuMikuDance/UserFile/Output/output'
# Base filename of the final output videos (as opposed to temporary renders, such as splits)
# If you use the tmpfs trick, this should point to a permanent location
# Simply set the value to OUTPUT to make them the same
FINAL_OUTPUT = OUTPUT


## Misc ##
# Distance between the two eyes
# If set to -1, use the viewpoint bone model instead
# If rendering a non-VR video, this value will be ignored
PARALLAX = -1
# Your system's shortcut for minimizing windows
# See https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys for how to write it
MINIMIZE_SHORTCUT = 'win', 'pagedown'
# MMD launch command - you can just edit the three parts described below
LAUNCH_MMD = (
	'cd '
	'~/Projects/MikuMikuDance/'			# Path to the directory that contains the MMD .exe
	' && LANG=ja_JP.UTF-8 WINEPREFIX='
	'~/.WineMMD64'						# Path to the Wine prefix
	' WINEARCH=win64 wine '
	'MikuMikuDance.exe'					# Filename of the MMD .exe
)
# How long to wait for MMD to launch and be ready to use (in seconds)
MMD_LAUNCH_WAIT = 10.0
# How long to wait for the project to load and for MMD to become responsive (in seconds)
MMD_PROJECT_WAIT = 20.0


## Rendering settings ##
FPS = 60
# Start and end frames. Format as: (start, end)
RECORDING = (0, 8000)
# Render this many frames at a time - useful if the codec is AVI Raw
# Set this to 0 to render the whole project at once
SPLIT = 500
# The codec to use; set this to the position of the codec in the list shown by MMD
# For example, to use the first codec, set this to 1
# To use AVI Raw, set it to -1
CODEC_N = -1


## Screen positions ##
# Formatted as (x coordinate, y coordinate)
# X coordinates increase from left to right; Y coordinates increase from top to bottom
# Both coordinates must be whole numbers
# You can screenshot MMD when it's running and open the screenshot in an image editor
# to figure out the coordinates for each spot
# The example values work for a 1920x1080 screen with a 50px wide taskbar on the left,
# where MMD's "split view" is enabled, the editor takes up the top half of the screen,
# and the preview/position editing window takes up the bottom half
NOOP = 1700, 75  # Place on the main (editor) window which focuses it, e.g. the red bar at the top
CAMERA_FOLLOW_BONE = 505, 515  # Not necessary unless PARALLAX = -1
CAMERA_REGISTER = 540, 515  # Not necessary unless PARALLAX = -1
EQUIRECTANGULAR_RX = 975, 490  # Not used in this example config
EQUIRECTANGULAR_REGISTER = 1100, 510  # Not used in this example config
AVIOUT_FPS = 930, 450
AVIOUT_CODEC = 1125, 600


## Parts ##
# Each part is formatted as follows:
# ('NAME', x_offset, camera_x_rotation, camera_y_rotation, equirectangularx_x_rotation, equirectangularx_y_rotation)
# If you use the viewpoint bone (i.e. PARALLAX = -1): set x_offset to -1 for left eye, and 1 for right eye
PARTS = [
	('', NOCHANGE, NOCHANGE, NOCHANGE, NOCHANGE, NOCHANGE)
]


## Post-processing ##
def post_process(n):
	return


split_files = []

def after_split(fp):
	# This function is called after each split has been rendered (only if SPLIT > 0).
	# ``fp`` is the path to the most recent split.
	postprocessing.convert_split(fp)


def merge_splits(n):
	# This function is called after the last split for a given part was rendered (only if SPLIT > 0).
	# It should call post_process() if necessary.
	# ``n`` is the index of ``PARTS`` that corresponds to the rendered part.
	postprocessing.concat_splits(OUTPUT + PARTS[n][0] + '.mp4')
