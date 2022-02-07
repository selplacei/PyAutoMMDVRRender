import pyautogui as pag
import config as cfg

INTRO = """
PyAutoMMDVRRender by selplacei
This is a simple PyAutoGUI script. It doesn't have any advanced capabilities
beyond pressing pre-defined buttons. Thus, it cannot detect certain things,
so in order for it to work, you must do the following:

1. Make sure that when MMD launches, it always launches with the same
   window size(s) and position(s). If you use "separate window" mode, make
   sure that one window doesn't cover the other.
   If you use multiple monitors, make sure that MMD launches on the primary monitor.
2. Think of which project you want to render.
3. Adjust the "config.py" file according to your configuration. Especially important
   are the screen positions of various buttons, which cannot be reached with the keyboard.
   To find out those positions, for example, you can take a screenshot and look at the
   coordinates in a program like GIMP or Krita.
4. Make sure that whenever the project is launched, there are no warnings like
   "model not found, specify its path", which would prevent the script from executing.
5. Make sure that the output files don't already exist on the system (to avoid the overwrite dialog).
6. Adjust the following values in your project to what you want them to be:
   - Camera view angle (if in doubt, use 90)
   - Camera position and angle (do not manually apply any parallax, and make sure that all angles are within -90 to 90)
   - EquirectangularX.x values other than Rx
7. Now make sure that whenever the project is launched, the "camera/light/accessory" model is selected
   along with its EquirectangularX.x accessory, and the project is ready to render.
8. Minimize all programs before launching the script. Once the last AVI file has started to render,
   the script has done its job and you can use your PC as normal.

To stop the script at any point, move the mouse to any corner of the primary screen.

Press ENTER to start the script or Ctrl+C to exit.
"""


def main():
	print(INTRO)
	try:
		input()
	except KeyboardInterrupt:
		print('Rendering canceled.')
		exit()
	
