# VL6180X
Controller class for the VL6180X laser ranging sensor.

The range is pretty limited, but it's a good sensor for detecting objects within a few centimeters.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- VL6180X
- Raspberry Pi Pico

### VL6180X Pinout
![VL6180X_pinout2.jpg](.assets%2FVL6180X_pinout2.jpg)

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### VL6180X Datasheet
[vl6180x_datasheet.pdf](.assets%2Fvl6180x_datasheet.pdf)


### LaserRangingSensorController Class
### Methods

#### `__init__(self, sda_pin, scl_pin, gesture_threshold=10, i2c_freq=400000)`
Initializes the `LaserRangingSensorController` with the specified I2C pins, gesture threshold, and I2C frequency.

- **Parameters:**
  - `sda_pin` (int): The pin number for the I2C data.
  - `scl_pin` (int): The pin number for the I2C clock.
  - `gesture_threshold` (int, optional): The threshold for gesture detection. Default is 10.
  - `i2c_freq` (int, optional): The I2C frequency. Default is 400000.

#### `get_distance(self)`
Gets the distance measured by the sensor.

- **Returns:**
  - `tuple`: A tuple containing the distance in millimeters and a boolean indicating if the distance is within range.

#### `continuous_get_distance(self, delay_ms=50)`
Continuously gets the distance measured by the sensor.

- **Parameters:**
  - `delay_ms` (int, optional): The delay in milliseconds between measurements. Default is 50 ms.

- **Yields:**
  - `tuple`: A tuple containing the distance in millimeters and a boolean indicating if the distance is within range.
