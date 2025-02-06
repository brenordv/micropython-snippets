# MQ-2 Smoke Detector Sensor
This project is a smoke detection system that uses a Raspberry Pi Pico and an MQ-2 gas sensor to monitor the concentration of smoke.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- Raspberry Pi Pico
- MQ-2 Gas Sensor

### MQ-2 Sensor Pinout
![mq2-pinout.jpg](.assets%2Fmq2-pinout.jpg)

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### MQ-2 Sensor Datasheet
[mq2.pdf](.assets%2FMQ2.pdf)

### SmokeDetectorSensor Class
### Methods

#### `__init__(self, pin, rl_value=5.0, r0=0.5, m=-0.45, b=1.4, voltage_ref=3.3, adc_max=65535, err_return_value=0)`
Initializes the `SmokeDetectorSensor` with the specified pin and calibration values.

- **Parameters:**
  - `pin` (int): The GPIO pin number to which the MQ-2 sensor is connected.
  - `rl_value` (float, optional): The load resistance value in kOhms. Default is 5.0.
  - `r0` (float, optional): The sensor resistance in clean air in kOhms. Default is 0.5.
  - `m` (float, optional): The slope from the log-log calibration curve. Default is -0.45.
  - `b` (float, optional): The intercept from the log-log calibration curve. Default is 1.4.
  - `voltage_ref` (float, optional): The reference voltage of the ADC. Default is 3.3.
  - `adc_max` (int, optional): The maximum value of the ADC. Default is 65535.
  - `err_return_value` (float, optional): The value to return in case of an error. Default is 0.

#### `read_raw_value(self)`
Reads the raw ADC value (0 to 65535) from the sensor.

- **Returns:**
  - `int`: The raw ADC value.

#### `read_ppm(self, raw_value=None)`
Converts the raw ADC value to an estimated gas concentration in PPM using the sensor's calibration curve.

- **Parameters:**
  - `raw_value` (int, optional): The raw ADC value. If not provided, it reads the value from the sensor.

- **Returns:**
  - `float`: The gas concentration in PPM.

#### `read_normalized(self, raw_value=None)`
Converts the raw ADC value to a normalized value between 0.0 and 1.0.

- **Parameters:**
  - `raw_value` (int, optional): The raw ADC value. If not provided, it reads the value from the sensor.

- **Returns:**
  - `float`: The normalized value.

#### `read(self)`
Reads the raw ADC value, PPM value, and normalized value.

- **Returns:**
  - `dict`: A dictionary containing the raw ADC value, PPM value, and normalized value.

## Example output
```text
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
PPM: 0.00, Normalized: 0.000
```
