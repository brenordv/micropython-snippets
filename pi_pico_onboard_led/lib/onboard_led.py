import time
import machine


class OnboardLED:
    """
    A class to control the onboard LED on the Raspberry Pi Pico W using MicroPython.

    The Pico W's onboard LED is accessed via the "LED" identifier.
    If you're using a different board (e.g., the original Pico), you might need
    to change the pin identifier (e.g., use 25).

    Example usage:
        led = OnboardLED()  # Initialize the LED (default uses "LED" for Pico W)
        led.on()           # Turn the LED on
        led.off()          # Turn the LED off
        led.toggle()       # Toggle the LED state
    """

    def __init__(self, pin_identifier="LED"):
        """
        Initialize the OnboardLED.

        Args:
            pin_identifier (str/int): Identifier for the LED pin.
                                      Default is "LED" for Pico W.
        """
        self.led = machine.Pin(pin_identifier, machine.Pin.OUT)

    def on(self):
        """Turn the LED on."""
        self.led.value(1)

    def off(self):
        """Turn the LED off."""
        self.led.value(0)

    def toggle(self):
        """Toggle the LED state."""
        self.led.value(not self.led.value())

    def blink(self, times=5, delay=0.5):
        """Blink the LED a specified number of times with the given delay (in seconds)."""
        for _ in range(times):
            self.on()
            time.sleep(delay)
            self.off()
            time.sleep(delay)
