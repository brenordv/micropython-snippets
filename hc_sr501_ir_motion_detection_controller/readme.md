# HC-SR501 IR Motion Detection Controller
A super simple controller for the HC-SR501 IR Motion Detection Sensor.

To use this, copy the `lib` folder to your project.

## Hardware
- HC-SR501 IR Motion Detection Sensor
- Raspberry Pi Pico

## HC-SR501 IR Motion Detection Sensor Pinout
![HC-SR501-IR-Motion-Detection-Sensor-Pinout.png](.assets%2FHC-SR501-IR-Motion-Detection-Sensor-Pinout.png)

## Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

## HC-SR501 Datasheet
[HC-SR501_datasheet.pdf](.assets%2FHC-SR501_datasheet.pdf)

### InfraredMotionSensorController Class
### Methods

#### `__init__(self, sensor_pin)`
Initializes the `InfraredMotionSensorController` with the specified sensor pin.

- **Parameters:**
  - `sensor_pin` (int): The pin number for the IR motion sensor.

#### `is_motion_detected(self)`
Checks if motion is detected by the sensor.

- **Returns:**
  - `bool`: `True` if motion is detected, otherwise `False`.

#### `continuous_motion_detection(self, delay_ms=50)`
Continuously checks for motion detection and yields the result.

- **Parameters:**
  - `delay_ms` (int, optional): The delay in milliseconds between each check. Default is 50 ms.

- **Yields:**
  - `bool`: `True` if motion is detected, otherwise `False`.
