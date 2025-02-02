# OnboardLED MicroPython Library

The `OnboardLED` class is a simple MicroPython library designed to control the onboard LED of the Raspberry Pi Pico W. It provides methods to turn the LED on, turn it off, toggle its current state, and blink the LED with customizable timing.

## Overview

The Raspberry Pi Pico W has a built-in LED that can be controlled using the `"LED"` identifier in MicroPython. This library wraps that functionality in an easy-to-use class, making it straightforward to integrate LED control into your projects.

## Features

- **Turn On**: Switch the LED on.
- **Turn Off**: Switch the LED off.
- **Toggle**: Change the LED state from on to off or vice versa.
- **Blink**: Blink the LED a specified number of times with a configurable delay between on and off states.

## How It Works

- **Hardware Access**: The class uses MicroPython's `machine.Pin` to interact with the hardware. The onboard LED on the Pico W is accessed via the special identifier `"LED"`.
- **Methods**: Each method (`on`, `off`, `toggle`, and `blink`) manipulates the pin's value to control the LED.
- **Blink Functionality**: The `blink` method uses a loop combined with `time.sleep()` to create a delay between toggling the LED on and off.

## Requirements

- **Hardware**: Raspberry Pi Pico W (or a similar board; note that for boards like the original Pico, you might need to change the pin identifier to the correct GPIO, such as `25`).
- **Software**: [MicroPython](https://micropython.org/) installed on your device.

## Installation
Just copy the `lib` folder to your board.

## Usage

Below is a quick example demonstrating how to use the `OnboardLED` class:

```python
import time
import machine
from lib.onboard_led import OnboardLED  # Ensure onboard_led.py is in your project directory

# Create an instance of OnboardLED (uses "LED" by default for Pico W)
led = OnboardLED()

# Turn the LED on
led.on()
time.sleep(1)

# Turn the LED off
led.off()
time.sleep(1)

# Toggle the LED state
led.toggle()
time.sleep(1)

# Blink the LED 5 times with a 0.5-second delay between toggles
led.blink(times=5, delay=0.5)
```