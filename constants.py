class PATHS:
	# Paths must be absolute
	PROJECT = '/mnt/projects/MikuMikuDance/UserFile/vrtest3.pmm'
	OUTPUT = '/mnt/projects/MikuMikuDance/UserFile/Output'
	OUTPUT_FILENAME = 'vrtest2_auto'


class MISC:
	PARALLAX = 0.8  # Distance between the two eyes
	MINIMIZE_SHORTCUT = 'win', 'pageup'  # See https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys


class RENDERING:
	FPS = 60
	RECORDING = 0, 8000  # Format as: (start, end)
	CODEC_N = 19  # First codec = 1


class POSITIONS:
	NOOP = 200, 75  # Place on the MAIN window which focuses it, e.g. the red bar at the top
	AVIOUT_FPS = 930, 450
	AVIOUT_CODEC = 1125, 600
