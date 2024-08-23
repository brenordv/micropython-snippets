# Pico board as a HID device
This is a simple snippet that, when executed, will:
1. Open notepad
2. Write some text to it.

This is done by simulating the actions of a user typing it.

# Attention
1. This code only works on Windows machine;
2. The code is not optimized, it is just a proof of concept;
3. This snippet will only work on `CircuitPython`. `Micropython` doesn't have the `usb_hid` module;
4. Please, don't use this to create anything evil;
5. Use this code at your own risk. I'm not responsible for any damage caused by it in any way, shape, or form.

# Installation
Just copy the `lib` folder to your board.
