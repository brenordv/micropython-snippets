import board
import busio
import time
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from lib.apds9960_controller import GestureDetectionController


# Set up I2C
i2c = busio.I2C(scl=board.GP5, sda=board.GP4, frequency=400000)  # Adjust GP pins according to your board

# Set up HID
keyboard = Keyboard(usb_hid.devices)

# Initialize the controllers
gesture_controller = GestureDetectionController(i2c)
has_windows_to_restore = False

# Testing gesture detection
print("Starting gesture detection")
for gesture in gesture_controller.continuous_read_gesture(only_known_gestures=True, detection_threshold=300):
    if gesture == "Left":
        keyboard.press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.LEFT_ARROW)
        keyboard.release_all()
        print(f"Gesture detected: {gesture} - Moving to the desktop on the left")

    elif gesture == "Right":
        keyboard.press(Keycode.CONTROL, Keycode.WINDOWS, Keycode.RIGHT_ARROW)
        keyboard.release_all()
        print(f"Gesture detected: {gesture} - Moving to the desktop on the right")

    elif gesture == "Down":
        keyboard.press(Keycode.WINDOWS, Keycode.D)
        keyboard.release_all()
        has_windows_to_restore = True
        print(f"Gesture detected: {gesture} - Sending WINDOWS + D")

    elif gesture == "Up" and has_windows_to_restore:
        has_windows_to_restore = False
        keyboard.press(Keycode.WINDOWS, Keycode.D)
        keyboard.release_all()
        print(f"Gesture detected: {gesture} - Sending WINDOWS + D because previous gesture was Down")

    # Brief delay to avoid sending commands too rapidly
    time.sleep(0.1)
