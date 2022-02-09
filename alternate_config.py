# Alternate example config - illustrates usage of the viewpoint bone and another way to post-process
# To apply it, rename the original config.py to something else, and this file to config.py

## Paths and filenames ##
# Paths must be absolute and cannot contain characters that can't be typed on a keyboard
PROJECT = '/mnt/projects/MikuMikuDance/UserFile/vrtest2.pmm'
OUTPUT = '/mnt/projects/MikuMikuDance/UserFile/Output/vrtest2_auto_'

## Misc ##
# Distance between the two eyes
PARALLAX = -1
# Your system's shortcut for minimizing windows
# See https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
MINIMIZE_SHORTCUT = 'win', 'pagedown'
# Set your Wine prefix and path to MMD here.
LAUNCH_MMD = 'cd /mnt/projects/MikuMikuDance/ && LANG=ja_JP.UTF-8 WINEPREFIX=~/.WineMMD64 WINEARCH=win64 wine MikuMikuDance.exe'
MMD_LAUNCH_WAIT = 10.0
MMD_PROJECT_WAIT = 20.0
MMD_PART_WAIT = 3.5 * 60 * 60 + 10  # How long to wait before starting another MMD instance
MMD_PART_TIMEOUT = 3.5 * 60 * 60  # How long to wait until terminating an existing MMD instance

## Rendering ##
FPS = 60
RECORDING = 0, 8400  # Format as: (start, end)
CODEC_N = 19  # First codec = 1

## Screen positions ##
NOOP = 1700, 75  # Place on the MAIN window which focuses it, e.g. the red bar at the top
CAMERA_FOLLOW_BONE = 505, 515  # Not necessary unless PARALLAX = -1
CAMERA_REGISTER = 540, 515 # Not necessary unless PARALLAX = -1
EQUIRECTANGULAR_RX = 975, 490
EQUIRECTANGULAR_REGISTER = 1100, 510
AVIOUT_FPS = 930, 450
AVIOUT_CODEC = 1125, 600

## Parts ##
# Each part is formatted as follows:
# ('NAME', x_offset, camera_x_rotation, camera_y_rotation, equirectangularx_x_rotation, equirectangularx_y_rotation)
# If you use the viewpoint bone: set x_offset to -1 for left eye, and 1 for right eye
PARTS = [
	('L_TOP', -1, -90, 0, -90, 0),
	('R_TOP', 1, -90, 0, -90, 0),
	('L_BOTTOM', -1, 90, 0, 90, 0 ),
	('R_BOTTOM', 1, 90, 0, 90, 0),
	('L_FRONT', -1, 0, 0, 0, 0),
	('R_FRONT', 1, 0, 0, 0, 0),
	('L_LEFT', -1, 0, 90, 0, 90),
	('R_LEFT', 1, 0, 90, 0, 90),
	('L_RIGHT', -1, 0, -90, 0, -90),
	('R_RIGHT', 1, 0, -90, 0, -90),
]

## Post-processing ##
# If you don't want any post-processing, remove the # sign just below "def post_process(n):", before "return"
# This is a Python function. It's called every time an MMD instance is terminated (which, hopefully,
# means that a part has just finished rendering). Its only argument is an integer indicating
# the index of the last finished render (for example, according to the PARTS value provided above,
# this function will be called with n = 4 as soon as L_RIGHT has finished rendering).
# This can be useful, for example, to stitch parts before new parts are generated to save disk space.
# Technical note: this will run in a different thread than the main script, so the timers for
# starting a new MMD instance will work as normal. This means that you can run CPU-intensive tasks
# in parallel with MMD renders. However, if you use a GPU-intensive task (such as stiching videos),
# you'll likely not want a render to run at the same time. You can achieve this by setting
# MMD_PART_WAIT to the sum of MMD_PART_TIMEOUT and the expected maximum time for post-processing
# to complete, leaving some free room between renders. However, as this will leave the same long
# break between each render, you may want to dynamically adjust MMD_PART_WAIT within this function.
# When this function is called, the timer for MMD_PART_WAIT is already running and can't be changed;
# if you change it within this function, it'll affect the next render.
# The provided example uses ffmpeg to stitch the eyes for each direction, leaving the chroma keying to the user.
def post_process(n):
	if n % 2:
		MMD_PART_WAIT = 3.5 * 60 * 60 + 10
	else:
		MMD_PART_WAIT = 4 * 60 * 60
		import subprocess
		import os
		file_l = OUTPUT + PARTS[n - 1][0] + '.avi'
		file_r = OUTPUT + PARTS[n][0] + '.avi'
		p = subprocess.run([
			'ffmpeg', '-i', file_l, '-i', file_r, '-filter_complex', 'hstack',
			'-vcodec', 'libx264', file_l.replace('L_', 'ALL_').replace('.avi', '.mp4')
		])
		if p.returncode == 0:
			os.remove(file_l)
			os.remove(file_r)
