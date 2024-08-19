# [DS18X20] Temperature Sensor Controller
This project is a simple controller for a temperature and humidity sensor.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- DS18X20 Sensor
- Raspberry Pi Pico

### DS18X20 Sensor Pinout
![DS18X20-waterproof-temperature-sensor.jpg](.assets%2FDS18X20-waterproof-temperature-sensor.jpg)

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### DS18X20 Sensor Datasheet
[ds18b20.pdf](.assets%2Fds18b20.pdf)

### TemperatureController Class
### Methods

#### `__init__(self, pin, temp_offset=0)`
Initializes the `TemperatureController` with the specified pin and temperature offset.

- **Parameters:**
  - `pin` (int): The GPIO pin number to which the DS18X20 sensor is connected.
  - `temp_offset` (float, optional): The temperature offset for calibration. Default is 0.

#### `measure(self)`
Measures the temperature using the DS18X20 sensor.

- **Returns:**
  - `bool`: `True` if the measurement is successful, otherwise `False`.

#### `get_temperature(self)`
Gets the last measured temperature.

- **Returns:**
  - `float`: The last measured temperature, or `None` if no measurement is available.

#### `set_temp_calibration(self, offset)`
Sets the temperature calibration offset.

- **Parameters:**
  - `offset` (float): The temperature offset for calibration.

#### `get_readings(self)`
Gets the current temperature reading.

- **Returns:**
  - `dict`: A dictionary containing the temperature and timestamp, or `None` if the measurement fails.

#### `get_last_error(self)`
Gets the last error message.

- **Returns:**
  - `str`: The last error message, or an empty string if no error occurred.

#### `continuous_measurement(self, max_consecutive_failures=10, delay_ms=1000)`
Continuously measures the temperature, yielding the results.

- **Parameters:**
  - `max_consecutive_failures` (int, optional): The maximum number of consecutive failures allowed before raising an error. Default is 10.
  - `delay_ms` (int, optional): The delay in milliseconds between measurements. Default is 1000 ms.

- **Yields:**
  - `tuple`: A tuple containing a boolean indicating success, the temperature, and the timestamp.

- **Raises:**
  - `Ds18x20Error`: If the maximum number of consecutive failures is reached.

#### `measure_with_retry(self, retries=3, delay_ms=1000)`
Measures the temperature with retries.

- **Parameters:**
  - `retries` (int, optional): The number of retries. Default is 3.
  - `delay_ms` (int, optional): The delay in milliseconds between retries. Default is 1000 ms.

- **Returns:**
  - `dict`: A dictionary containing the temperature and timestamp, or `None` if the measurement fails.
