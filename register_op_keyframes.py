"""
How to abuse the Outside Parent feature to copy the effective (absolute) motion of one bone to another.
1. Select the desired model and bone to copy to. This bone should not follow any parent (a motherbone would work).
2. Ensure that there are no Disp/IK/OP keyframes in the destination model.
3. Turn on OP on the first frame, selecting the desired source bone as the parent.
4. Make sure that the destination bone has the correct offset
   (its current absolute coordinates will become relative to the source bone).
   If you want it to follow the source bone exactly, set all coordinates to 0.
5. Click "copy" in the bone manipulation pane while the first frame of the destination bone is selected.
   You have to do this even if the offset is (0, 0, 0).
6. Run the script.
7. Turn off OP on the first frame.
"""
from time import sleep
import pyautogui as pag


TOTAL_FRAMES = 500
KEYFRAME_FREQUENCY = 5

START_CLICKING_FRAMES_AT = 75

OP_BUTTON = 392, 1029
OP_TARGET_MODEL_DROPDOWN = 955, 499
FRAME_REGISTER_BUTTON = 983, 691
FRAME_SELECT_CURRENT = 1044, 203
FRAME_SELECT_NEXT_OFFSET = 13
BONE_PASTE_BUTTON = 513, 1021
BONE_REGISTER_BUTTON = 448, 1059


if __name__ == '__main__':
	sleep(5)
	current_frame = 0
	while current_frame <= TOTAL_FRAMES:
		pag.click(x=BONE_PASTE_BUTTON[0], y=BONE_PASTE_BUTTON[1])
		pag.click(x=BONE_REGISTER_BUTTON[0], y=BONE_REGISTER_BUTTON[1])
		pag.click(x=OP_BUTTON[0], y=OP_BUTTON[1])
		pag.click(OP_TARGET_MODEL_DROPDOWN)
		pag.press('home')
		pag.press('enter')
		pag.click(x=FRAME_REGISTER_BUTTON[0], y=FRAME_REGISTER_BUTTON[1])
		pag.press('escape')
		sleep(0.1)
		frame_increase = max(1, min(KEYFRAME_FREQUENCY, TOTAL_FRAMES - current_frame))
		if current_frame < START_CLICKING_FRAMES_AT:
			for _ in range(frame_increase):
				# Just using .press('right') doesn't do anything, for some reason.
				pag.keyDown('right')
				sleep(0.01)
				pag.keyUp('right')
				current_frame += 1
		else:
			pag.click(x=(FRAME_SELECT_CURRENT[0] + FRAME_SELECT_NEXT_OFFSET * frame_increase), y=FRAME_SELECT_CURRENT[1])
			current_frame += frame_increase
