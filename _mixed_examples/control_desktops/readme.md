# Controls (changes) Windows Desktops by using gestures
This example meshes two snippets:
- [APDS9960 Gesture, Proximity, RGB, and Light controller](../../apds9960_gesture_proximity_rgb_light_controller/readme.md)
- [Using Pico as a HID](../../pico_as_hid/readme.md)

The difference is that instead of just opening the `notepad`, and writing some text, in this snippet, we are changing
the desktops on Windows based on the gesture detected by the APDS9960 sensor:
- Up: Show all windows
- Down: Show desktop (minimize all windows)
- Left: Show previous desktop (if available, the desktop on the left)
- Right: Show next desktop (if available, the desktop on the right)

## Important notes
1. The code for `APDS9960` was converted from Micropython to CircuitPython, and stripped down to just the functionality
   needed for this example.

# Installation
1. Copy everything in the `lib` folder to your Pico (or compatible board).
2. Run the `main.py` script.

# Hardware
- Pico
- ADPS9960 Gesture Sensor

# OS
Board: CircuitPython
Host: Windows

# Demo
https://www.tiktok.com/@raccoon.ninja/video/7406227139390885125