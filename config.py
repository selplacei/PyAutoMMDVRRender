## Paths and filenames ##
# Paths must be absolute and cannot contain characters that can't be typed on a keyboard
PROJECT = '/mnt/projects/MikuMikuDance/UserFile/project.pmm'
OUTPUT = '/mnt/projects/MikuMikuDance/UserFile/Output/output'

## Misc ##
# Distance between the two eyes
# If set to -1, use the viewpoint bone model instead
PARALLAX = 0.8
# Your system's shortcut for minimizing windows
# See https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
MINIMIZE_SHORTCUT = 'win', 'pagedown'
# Set your Wine prefix and path to MMD here.
LAUNCH_MMD = 'LANG=ja_JP.UTF-8 WINEPREFIX=~/.WineMMD64 WINEARCH=win64 wine PATH_TO_MMD_EXE_HERE'
MMD_LAUNCH_WAIT = 10.0
MMD_PROJECT_WAIT = 20.0

## Rendering ##
FPS = 60
RECORDING = 0, 8000  # Format as: (start, end)
SPLIT = 0  # 0 for no split
CODEC_N = 19  # First codec = 1; -1 for AVI Raw

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
	('L_TOP', -(PARALLAX / 2), -90, 0, -90, 0),
	('L_BOTTOM', -(PARALLAX / 2), 90, 0, 90, 0 ),
	('L_FRONT', -(PARALLAX / 2), 0, 0, 0, 0),
	('L_LEFT', -(PARALLAX / 2), 0, 90, 0, 0),
	('L_RIGHT', -(PARALLAX / 2), 0, -90, 0, 0),
	('R_TOP', PARALLAX / 2, -90, 0, -90, 0),
	('R_BOTTOM', PARALLAX / 2, 90, 0, 90, 0),
	('R_FRONT', PARALLAX / 2, 0, 0, 0, 0),
	('R_LEFT', PARALLAX / 2, 0, 90, 0, 0),
	('R_RIGHT', PARALLAX / 2, 0, -90, 0, 0),
]

## Post-processing ##
# If you don't want any post-processing, remove the # sign just below "def post_process(n):", before "return"
# This is a Python function. It's called every time an MMD instance is terminated (which, hopefully,
# means that a part has just finished rendering). Its only argument is an integer indicating
# the index of the last finished render (for example, according to the PARTS value provided above,
# this function will be called with n = 4 as soon as L_RIGHT has finished rendering).
# This can be useful, for example, to stitch parts before new parts are generated to save disk space.
# The provided example uses ffmpeg to stitch the parts for each eye and convert the result to h246 mp4.
def post_process(n):
	#return
	if n == 4:
		# Stitch the left eye
		import subprocess
		import os
		FFMPEG_FILTER = "[1]split[m][a];[a]geq='if(gt(lum(X,Y),16),255,0)',hue=s=0[al];[m][al]alphamerge[ovr];[0][ovr]overlay"
		process = subprocess.run(
			[
				'ffmpeg',
				'-i', OUTPUT + PARTS[0][0] + '.avi',
				'-i', OUTPUT + PARTS[1][0] + '.avi',
				'-filter_complex', FFMPEG_FILTER,
				'-i', OUTPUT + PARTS[2][0] + '.avi',
				'-filter_complex', FFMPEG_FILTER,
				'-i', OUTPUT + PARTS[3][0] + '.avi',
				'-filter_complex', FFMPEG_FILTER,
				'-i', OUTPUT + PARTS[4][0] + '.avi',
				'-filter_complex', FFMPEG_FILTER,
				'-vcodec', 'libx264',
				OUTPUT + 'L_ALL.mp4'
			]
		)
		# If stitching failed, bail out, as there may not be enough disk space to render the right eye
		if process.returncode != 0:
			print('Post-processing failed!')
			os._exit(1)
		for part in PARTS[:5]:
			os.remove(OUTPUT + part[0] + '.avi')
	elif n == 9:
		# Stitch the right eye
		import subprocess
		import os
		process = subprocess.run(
			[
				'ffmpeg',
				'-i', OUTPUT + PARTS[5][0] + '.avi',
				'-i', OUTPUT + PARTS[6][0] + '.avi',
				'-filter_complex', FFMPEG_FILTER,
				'-i', OUTPUT + PARTS[7][0] + '.avi',
				'-filter_complex', FFMPEG_FILTER,
				'-i', OUTPUT + PARTS[8][0] + '.avi',
				'-filter_complex', FFMPEG_FILTER,
				'-i', OUTPUT + PARTS[9][0] + '.avi',
				'-filter_complex', FFMPEG_FILTER,
				'-vcodec', 'libx264',
				OUTPUT + 'R_ALL.mp4'
			]
		)
		# This time, if stitching failed, there's nothing to terminate - just don't delete the AVIs
		if process.returncode == 0:
			for part in PARTS[5:]:
				os.remove(OUTPUT + part[0] + '.avi')
		# The video still needs sound added to it, which is beyond the scope of this function,
		# so we'll leave stiching the two eyes up to the user as well


# This function is called after each split has been rendered (only if SPLIT > 0).
# ``fp`` is the path to the most recent split.
def after_split(fp):
	return


# This function is called after the last split for a given part has been rendered (only if SPLIT > 0).
# It should call post_process() if necessary.
# ``n`` is the index of ``PARTS`` that corresponds to the rendered part.
def merge_splits(n):
	return
