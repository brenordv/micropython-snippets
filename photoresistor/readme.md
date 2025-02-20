# Photoresistor Library
This project provides a simple library for interfacing with a photoresistor using an ADC pin on a microcontroller.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- Raspberry Pi Pico
- A photoresistor

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### Photoresistor Datasheet
[Datasheet](.assets%2FPhotoresistor-5516-datasheet.pdf)

### Photoresistor Class
### Methods

#### `__init__(self, adc_pin, volt=3.3)`
Initializes the `Photoresistor` instance.

- **Parameters:**
  - `adc_pin` (int): The ADC pin number where the photoresistor is connected.
  - `volt` (float): The reference voltage for the ADC (default is 3.3V).

#### `read(self)`
Reads the current value from the photoresistor.

- **Returns:**
  - `float`: The voltage corresponding to the light intensity.

## Example Usage
```python
import time
from lib.photoresistor import Photoresistor

p = Photoresistor(26)

while True:
    val = p.read()
    print(f"Light value: {val}")
    time.sleep(0.1)
```
