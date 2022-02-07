## Paths and filenames ##
# Paths must be absolute and cannot contain characters that can't be typed on a keyboard
PROJECT = '/mnt/projects/MikuMikuDance/UserFile/project.pmm'
OUTPUT = '/mnt/projects/MikuMikuDance/UserFile/Output/output'

## Misc ##
# Distance between the two eyes
PARALLAX = 0.8
# Your system's shortcut for minimizing windows
# See https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
MINIMIZE_SHORTCUT = 'win', 'pagedown'
# Set your Wine prefix and path to MMD here.
LAUNCH_MMD = 'LANG=ja_JP.UTF-8 WINEPREFIX=~/.WineMMD64 WINEARCH=win64 wine PATH_TO_MMD_EXE_HERE'
MMD_LAUNCH_WAIT = 10.0
MMD_PROJECT_WAIT = 20.0
MMD_PART_WAIT = 30 * 60  # How long to wait before starting another MMD instance
MMD_PART_TIMEOUT = 60 * 60  # How long to wait until terminating an existing MMD instance

## Rendering ##
FPS = 60
RECORDING = 0, 8000  # Format as: (start, end)
CODEC_N = 19  # First codec = 1

## Screen positions ##
NOOP = 200, 75  # Place on the MAIN window which focuses it, e.g. the red bar at the top
EQUIRECTANGULAR_RX = 975, 490
EQUIRECTANGULAR_REGISTER = 1100, 510
AVIOUT_FPS = 930, 450
AVIOUT_CODEC = 1125, 600
