from dataclasses import dataclass
from time import sleep
from threading import Thread
import subprocess
import pyautogui as pag
import config as cfg

@dataclass
class Part:
	suffix: str
	offset: float
	rot_x: int
	rot_y: int
	eqr_x: int

PARTS = [
	Part('L_TOP', -(cfg.PARALLAX / 2), -90, 0, -90),
	Part('L_BOTTOM', -(cfg.PARALLAX / 2), 90, 0, 90),
	Part('L_FRONT', -(cfg.PARALLAX / 2), 0, 0, 0),
	Part('L_LEFT', -(cfg.PARALLAX / 2), 0, 90, 0),
	Part('L_RIGHT', -(cfg.PARALLAX / 2), 0, -90, 0),
	Part('R_TOP', cfg.PARALLAX / 2, -90, 0, -90),
	Part('R_BOTTOM', cfg.PARALLAX / 2, 90, 0, 90),
	Part('R_FRONT', cfg.PARALLAX / 2, 0, 0, 0),
	Part('R_LEFT', cfg.PARALLAX / 2, 0, 90, 0),
	Part('R_RIGHT', cfg.PARALLAX / 2, 0, -90, 0),
]

INTRO = f"""PyAutoMMDVRRender by selplacei
This is a simple PyAutoGUI script.
It doesn't have any advanced capabilities beyond pressing pre-defined buttons.
Thus, it cannot detect anything, so in order for it to work,
you must do the following:

1. Make sure that when MMD launches,
   it always launches with the same window size(s) and position(s).
   If you use "separate window" mode,
   make sure that one window doesn't cover the other.
   If you use multiple monitors,
   make sure that MMD launches on the primary monitor.
   If you use KDE, this can be done for sure using
   "Special Window Settings" (Position, Size, Screen)
2. Think of which project you want to render.
3. Adjust the "config.py" file according to your configuration.
   Especially important are the screen positions of various buttons,
   which cannot be reached with the keyboard.
   To find out those positions, for example, you can take a screenshot
   and look at the coordinates in a program like GIMP or Krita.
   The top left corner of the screen is (0, 0), and values increase from there.
4. Make sure that whenever the project is launched,
   there are no warnings like "model not found, specify its path" etc.,
   which would prevent the script from executing correctly.
5. Make sure that the output files don't already exist on the system
   (to avoid dealing with the overwrite dialog).
6. Adjust the following values in your project to what you want them to be:
   - Camera view angle (if in doubt, use 90)
   - Camera position and angle
     * Do not manually apply any parallax
	 * Make sure that all angles are within -90 to 90
   - EquirectangularX.x values other than Rx
   - Screen size
7. Now make sure that whenever the project is launched,
   the "camera/light/accessory" model is selected
   along with its EquirectangularX.x accessory,
   and the project is ready to render.
8. Minimize all programs (except the terminal) before launching the script.
   Once the last AVI file has started to render,
   the script has done its job and you can use your PC as normal.

This script doesn't attempt to deal with errors, so things may go south.
To stop the script at any point, move the mouse to any corner of the screen.

Minimum time to complete: {round(cfg.MMD_PART_WAIT * len(PARTS) // 60 / 60, 1)} hours
Maximum time to complete: {round(cfg.MMD_PART_TIMEOUT * len(PARTS) // 60 / 60, 1)} hours
Press ENTER to start the script or Ctrl+C to exit."""

processes = []


def main():
	print(INTRO)
	try:
		input()
	except KeyboardInterrupt:
		print('Rendering canceled.')
		exit()
	pag.PAUSE = 0.2
	for _ in range(4):
		# Minimize (hopefully) all windows
		minimize()
		sleep(0.1)
	for part in PARTS:
		print(f'Starting {part.suffix}')
		minimize()
		load_mmd()
		adjust_camera(part.offset, part.rot_x, part.rot_y)
		adjust_eqr(part.eqr_x)
		sleep(1)
		render(part.suffix)
		print(f'Rendering {part.suffix} started')
		if part != PARTS[-1]:
			# If this is the last render, my job is done
			# Otherwise, automatically close the MMD instance
			p = processes.pop(0)
			Thread(target=timeout, args=(p, part.suffix)).start()
			sleep(cfg.MMD_PART_WAIT)
		pag.PAUSE += 0.4  # Accomodate for potential lag from multiple running instances
	print('Script finished')


def timeout(p, name):
	sleep(cfg.MMD_PART_TIMEOUT)
	p.terminate()
	print(f'Terminating {name}')


def minimize():
	# To be safe, minimize 3 times: twice for MMD's windows and once for the terminal
	for _ in range(3):
		pag.hotkey(*cfg.MINIMIZE_SHORTCUT)


def refocus():
	pag.click(x=cfg.NOOP[0], y=cfg.NOOP[1])


def load_mmd():
	processes.append(subprocess.Popen(['/bin/sh', '-c', cfg.LAUNCH_MMD], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
	sleep(cfg.MMD_LAUNCH_WAIT)
	refocus()
	pag.hotkey('alt', 'f')
	pag.press('o')
	sleep(1)
	for _ in range(5):
		pag.press('tab')
	pag.press('down')
	pag.press('end')
	pag.press('enter')
	pag.press('tab')
	for subdir in cfg.PROJECT.split('/')[:-1]:
		pag.write(subdir, interval=0.02)
		pag.press('enter')
		sleep(0.05)
	pag.press('tab')
	pag.write(cfg.PROJECT.split('/')[-1], interval=0.02)
	pag.press('enter')
	sleep(cfg.MMD_PROJECT_WAIT)
	refocus()


def adjust_camera(offset, rot_x, rot_y):
	# Assume an opened MMD window in normal state
	pag.hotkey('alt', 'd')
	pag.press('c')
	pag.hotkey('alt', 'd')
	pag.press('g')
	pag.press('tab')
	pag.write(str(offset))
	for _ in range(6):
		pag.press('tab')
	pag.write(str(rot_x))
	pag.press('tab')
	pag.press('tab')
	pag.write(str(rot_y))
	pag.press('enter')


def adjust_eqr(rx):
	pag.click(x=cfg.EQUIRECTANGULAR_RX[0], y=cfg.EQUIRECTANGULAR_RX[1])
	for _ in range(5):
		pag.press('delete')
		pag.press('backspace')
	pag.write(str(rx))
	pag.press('enter')
	pag.click(x=cfg.EQUIRECTANGULAR_REGISTER[0], y=cfg.EQUIRECTANGULAR_REGISTER[1])
	
	
def render(output_suffix):
	# Assume an opened MMD window in normal state
	refocus()
	pag.hotkey('alt', 'f')
	pag.press('v')
	for _ in range(4):
		pag.press('tab')
	pag.press('down')
	pag.press('end')
	pag.press('enter')
	pag.press('tab')
	for subdir in cfg.OUTPUT.split('/')[:-1]:
		pag.write(subdir, interval=0.02)
		pag.press('enter')
		sleep(0.05)
	pag.press('tab')
	pag.write(cfg.OUTPUT.split('/')[-1] + output_suffix + '.avi', interval=0.02)
	pag.press('enter')
	sleep(0.2)
	# File selected, adjust AVI-out settings
	pag.click(x=cfg.AVIOUT_FPS[0], y=cfg.AVIOUT_FPS[1])
	pag.press('delete')
	pag.press('backspace')
	pag.press('delete')
	pag.press('backspace')
	pag.write(str(cfg.FPS))
	pag.press('tab')
	pag.write(str(cfg.RECORDING[0]))
	pag.press('tab')
	pag.write(str(cfg.RECORDING[1]))
	pag.click(x=cfg.AVIOUT_CODEC[0], y=cfg.AVIOUT_CODEC[1])
	pag.press('home')
	for _ in range(cfg.CODEC_N - 1):
		pag.press('down')
	pag.press('enter')
	pag.press('enter')


if __name__ == '__main__':
	main()
