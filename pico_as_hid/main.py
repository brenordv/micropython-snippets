import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize the keyboard
kbd = Keyboard(usb_hid.devices)

def type_string(string):
    for char in string:
        if char.isupper():  # For uppercase letters
            kbd.press(Keycode.SHIFT, getattr(Keycode, char.upper()))
            kbd.release_all()
        elif char == ' ':  # For space
            kbd.press(Keycode.SPACE)
            kbd.release_all()
        elif char == '!':  # For exclamation mark
            kbd.press(Keycode.SHIFT, Keycode.ONE)  # Shift + 1
            kbd.release_all()
        elif char == '.':  # For period
            kbd.press(Keycode.PERIOD)
            kbd.release_all()
        elif char == ',':  # For comma
            kbd.press(Keycode.COMMA)
            kbd.release_all()
        elif char == '\n':  # For new line
            kbd.press(Keycode.ENTER)
            kbd.release_all()
        elif char == '\'':  # For single quote
            kbd.press(Keycode.QUOTE)
            kbd.release_all()
        elif char == '"':  # For double quote
            kbd.press(Keycode.SHIFT, Keycode.QUOTE)  # Shift + '
            kbd.release_all()
        elif char == '?':  # For question mark
            kbd.press(Keycode.SHIFT, Keycode.SLASH)  # Shift + /
            kbd.release_all()
        else:  # For lowercase letters
            kbd.press(getattr(Keycode, char.upper()))
            kbd.release_all()

# Open Run dialog (Win + R)
kbd.press(Keycode.WINDOWS, Keycode.R)
kbd.release_all()

# Give time for Run dialog to open
time.sleep(0.5)

# Type 'notepad'
type_string("notepad")

# Press Enter to open Notepad
kbd.press(Keycode.ENTER)
kbd.release_all()
time.sleep(1)  # Wait for Notepad to open

# Type 'hello world'
type_string("""Hey there folks!
This is one of the reasons why you should NEVER plug in a random USB device into your computer.
This is a Pico board pretending to be a keyboard.

And I'm just writing this message, but this could easily be a malicious script that could do a lot of 
harm to your computer.

Stay safe out there!

Cheers!
""")

# Optional: Add a newline by pressing Enter
kbd.press(Keycode.ENTER)
kbd.release_all()
