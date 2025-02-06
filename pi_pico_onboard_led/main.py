import time

from lib.morse_led import MorseLED

led = MorseLED()

# Base functionality (Present on the OnboardLED class)
led.on()
time.sleep(1)
led.off()

led.toggle()
time.sleep(1)
led.toggle()

led.blink(times=5, delay=0.2)

# Speak in morse code
led.morse_code("SOS", 3)
