#!/usr/bin/env sh
export DISPLAY=":1"
Xvfb :1 -screen 0 1920x1080x24 &
kwin_x11 &
if [[ $1 == "--vnc" ]]; then
	x11vnc -display :1 -bg -nopw -listen localhost -xkb &
	DISPLAY=:0 vncviewer localhost:5900 &
fi
python PyAutoMMDVRRender/main.py --start
killall Xvfb
