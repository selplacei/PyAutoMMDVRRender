# Alternate example config - illustrates usage of the viewpoint bone and another way to post-process
# To apply it, rename the original config.py to something else, and this file to config.py

## Paths and filenames ##
# Paths must be absolute and cannot contain characters that can't be typed on a keyboard
PROJECT = '/mnt/projects/MikuMikuDance/UserFile/project.pmm'
OUTPUT = '/mnt/projects/MikuMikuDance/UserFile/Output/output_'

## Misc ##
# Distance between the two eyes
PARALLAX = -1
# Your system's shortcut for minimizing windows
# See https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
MINIMIZE_SHORTCUT = 'win', 'pagedown'
# Set your Wine prefix and path to MMD here.
LAUNCH_MMD = 'cd ~/MikuMikuDance && LANG=ja_JP.UTF-8 WINEPREFIX=~/.WineMMD64 WINEARCH=win64 wine MikuMikuDance.exe'
MMD_LAUNCH_WAIT = 10.0
MMD_PROJECT_WAIT = 20.0

## Rendering ##
FPS = 60
RECORDING = 0, 8400  # Format as: (start, end)
SPLIT = 500  # 0 for no split
CODEC_N = -1  # First codec = 1; -1 for AVI Raw

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
# This is a Python function. It's called every time an MMD instance is terminated (which, hopefully,
# means that a part has just finished rendering). Its only argument is an integer indicating
# the index of the last finished render.
# The provided example uses ffmpeg to stitch the eyes for each direction, leaving the chroma keying to the user.
def post_process(n):
	if n % 2 == 1:
		import subprocess
		import os
		file_l = OUTPUT + PARTS[n - 1][0] + '.mp4'
		file_r = OUTPUT + PARTS[n][0] + '.mp4'
		print('Running ffmpeg to stitch eyes together...')
		p = subprocess.run([
			'ffmpeg', '-i', file_l, '-i', file_r, '-filter_complex', 'hstack',
			'-vcodec', 'libx264', file_l.replace('L_', 'ALL_')
		])
		if p.returncode == 0:
			print('Done, removing the LEFT and RIGHT files')
			os.remove(file_l)
			os.remove(file_r)


split_files = []
# This function is called after each split has been rendered.
# ``fp`` is the path to the most recent split.
def after_split(fp):
	import subprocess
	import os
	print('Running ffmpeg to convert AVI to MP4...')
	p = subprocess.run([
			'ffmpeg', '-i', fp, '-vcodec', 'libx264', fp.replace('.avi', '.mp4')
		])
	if p.returncode == 0:
		print('Done, removing the AVI file')
		os.remove(fp)
		split_files.append(fp.replace('.avi', '.mp4'))


# This function is called after the last split for a given part has been rendered.
# It should call post_process if necessary.
# ``n`` is the index of ``PARTS`` that corresponds to the rendered part.
def merge_splits(n):
	from math import ceil
	import subprocess
	import os
	print('Running ffmpeg to merge splits...')
	with open(f'/tmp/PyAutoMMDVRRender{n}', 'w+') as f:
		for fp in split_files:
			f.write(f'file \'{fp}\'\n')
	p = subprocess.run([
		'ffmpeg', '-f', 'concat', '-safe', '0', '-i', f'/tmp/PyAutoMMDVRRender{n}', '-c', 'copy',
		OUTPUT + PARTS[n][0] + '.mp4'
	])
	if p.returncode == 0:
		print('Done, removing the original split files')
		for fp in split_files:
			os.remove(fp)
		split_files.clear()
		post_process(n)
