# HY-SRF05 Ultrasonic Distance Sensor
The HY-SRF05 is an ultrasonic distance sensor that can measure distances from 2cm to 450cm. 
It is a low-cost sensor that is easy to use and can be used in a variety of applications. 

The class UltraSonicDistanceSensor has a couple of convenience methods to get the distance in centimeters and inches.

To use this, copy the `lib` folder to your project.

## Hardware
- Raspberry Pi Pico
- HY-SRF05 Ultrasonic Distance Sensor (The HY-SRF04 is also compatible)

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### HY-SRF05 Pinout
![HY-SRF05-pinout.png](.assets%2FHY-SRF05-pinout.png)

### HY-SRF05 Datasheet
(That was as close as I could find)
[HY-SRF05.PDF](.assets%2FHY-SRF05.PDF)

### Example Wiring
![wiring_example.png](.assets%2Fwiring_example.png)

## Example output
```text
MPY: soft reboot
Initializing UltraSonic Distance Sensor...
Measuring distance...
Distance: 16.53 cm
Distance: 13.89 cm
Distance: 16.70 cm
Distance: 13.79 cm
Distance: 250.56 cm
Distance: 15.71 cm
Distance: 14.47 cm
Distance: 11.66 cm
Distance: 12.14 cm
Distance: 11.80 cm
Averaging distance...
Average Distance: 11.99 cm
Average Distance: 12.14 cm
Average Distance: 12.11 cm
Average Distance: 11.98 cm
Average Distance: 12.18 cm
Average Distance: 11.16 cm
Average Distance: 12.03 cm
Average Distance: 9.87 cm
Average Distance: 9.65 cm
Average Distance: 9.90 cm
Measuring distance...
Distance: 9.60 cm
Distance: 10.32 cm
Distance: 14.68 cm
Distance: 23.87 cm
Distance: 25.11 cm
Distance: 17.46 cm
Distance: 15.92 cm
Distance: 15.16 cm
Distance: 15.23 cm
Distance: 41.61 cm
Averaging distance...
Average Distance: 24.31 cm
Average Distance: 14.28 cm
Average Distance: 11.30 cm
Average Distance: 11.58 cm
Average Distance: 11.03 cm
Average Distance: 10.90 cm
Average Distance: 10.90 cm
Average Distance: 11.01 cm
Average Distance: 18.59 cm
Average Distance: 16.08 cm
Measuring distance...
Distance: 12.90 cm
Distance: 11.11 cm
Distance: 10.32 cm
Distance: 11.01 cm
Distance: 10.56 cm
Distance: 10.63 cm
Distance: 11.46 cm
Distance: 10.53 cm
Distance: 10.53 cm
```

## UltraSonicDistanceSensor Class
### Methods

#### `__init__(self, trigger_pin, echo_pin, settle_time=2)`
Initializes the `UltraSonicDistanceSensor` with the specified trigger and echo pins, and optional settle time.

- **Parameters:**
  - `trigger_pin` (int): The pin number for the trigger.
  - `echo_pin` (int): The pin number for the echo.
  - `settle_time` (int, optional): The time in seconds to allow the sensor to settle. Default is 2 seconds.

#### `measure_distance(self, verbose=False)`
Measures the distance using the ultrasonic sensor.

- **Parameters:**
  - `verbose` (bool, optional): If `True`, prints debug information. Default is `False`.

- **Returns:**
  - `float`: The measured distance in centimeters.

#### `average_distance(self, samples=3, delay_ms=60)`
Calculates the average distance over a specified number of samples.

- **Parameters:**
  - `samples` (int, optional): The number of samples to average. Default is 3.
  - `delay_ms` (int, optional): The delay in milliseconds between samples. Default is 60 ms.

- **Returns:**
  - `float`: The average measured distance in centimeters.
