# MQ-9 CO and Combustible Gas Detector
This project is a gas detection system that uses a Raspberry Pi Pico and an MQ-9 gas sensor to monitor the concentration of CO and combustible gases.
For this example, you can use `vcc`, `gnd`, and the `analog out` pin of the sensor to connect to the Pico.


## Installation
Just copy the `lib` folder to your board.

## Hardware
- Raspberry Pi Pico
- MQ-9 Gas Sensor

### MQ-9 Sensor Pinout
![MQ-9-gas-sensor.jpg](.assets%2Fmq-9-pinout.png)
> Got the image from [this site](https://quartzcomponents.com/blogs/electronics-projects/how-to-interface-mq9-gas-sensor-with-arduino).


### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)


### MQ-9 Sensor Datasheet
[MQ-9_Hanwei.pdf](.assets%2FMQ-9_Hanwei.pdf)


### GasDetectionSensor Class
### Methods

#### `__init__(self, pin, rl_value=20.0, r0=10.0, m=-0.38, b=1.33, voltage_ref=3.3, adc_max=65535, err_return_value=0)`
Initializes the `GasDetectionSensor` with the specified pin and calibration values.

- **Parameters:**
  - `pin` (int): The GPIO pin number to which the MQ-9 sensor is connected.
  - `rl_value` (float, optional): The load resistance value in kOhms. Default is 20.0.
  - `r0` (float, optional): The sensor resistance in clean air in kOhms. Default is 10.0.
  - `m` (float, optional): The slope from the log-log calibration curve. Default is -0.38.
  - `b` (float, optional): The intercept from the log-log calibration curve. Default is 1.33.
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
Based on the code in [main.py](main.py), the output will look like this:
```text
PPM: 51.05, Normalized: 0.294
PPM: 47.38, Normalized: 0.288
PPM: 45.20, Normalized: 0.285
PPM: 52.01, Normalized: 0.296
PPM: 52.49, Normalized: 0.296
PPM: 53.14, Normalized: 0.297
PPM: 47.97, Normalized: 0.289
PPM: 52.01, Normalized: 0.296
PPM: 52.33, Normalized: 0.296
PPM: 57.01, Normalized: 0.303
PPM: 56.15, Normalized: 0.302
PPM: 54.96, Normalized: 0.300
PPM: 49.34, Normalized: 0.292
PPM: 53.30, Normalized: 0.298
PPM: 52.17, Normalized: 0.296
PPM: 47.68, Normalized: 0.289
PPM: 47.68, Normalized: 0.289
PPM: 45.91, Normalized: 0.286
PPM: 49.65, Normalized: 0.292
PPM: 53.63, Normalized: 0.298
PPM: 49.80, Normalized: 0.292
PPM: 53.14, Normalized: 0.297
PPM: 49.80, Normalized: 0.292
PPM: 52.98, Normalized: 0.297
PPM: 52.49, Normalized: 0.296
PPM: 53.63, Normalized: 0.298
PPM: 49.96, Normalized: 0.293
PPM: 49.96, Normalized: 0.293
PPM: 45.05, Normalized: 0.284
PPM: 49.34, Normalized: 0.292
PPM: 46.64, Normalized: 0.287
PPM: 50.89, Normalized: 0.294
PPM: 47.53, Normalized: 0.289
PPM: 47.53, Normalized: 0.289
```