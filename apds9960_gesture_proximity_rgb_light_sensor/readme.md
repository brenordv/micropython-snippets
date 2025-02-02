# APDS-9960 Gesture, Proximity, RGB Light Controller
APDS-9960 is a digital RGB, ambient light, proximity and gesture sensor. In this snippet I created a couple of classes
to control the sensor.

They're not super comprehensive, but they work. 
IDK if it's because the light in mny room is awful, but the light sensor is a bit finicky.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- APDS-9960 Sensor
- Raspberry Pi Pico

### APDS-9960 Sensor Pinout
![APDS9960_pinout.png](.assets%2FAPDS9960_pinout.png)

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### APDS-9960 Sensor Datasheet
[Avago-APDS-9960-datasheet.pdf](.assets%2FAvago-APDS-9960-datasheet.pdf)

## Software
### GestureDetectionController Class
#### Methods
#### `__init__(self, i2c)`
Initializes the `GestureDetectionController` with the specified I2C interface.

- **Parameters:**
  - `i2c` (I2C): The I2C interface to communicate with the APDS-9960 sensor.

#### `read_gesture(self)`
Reads a single gesture from the sensor.

- **Returns:**
  - `str`: The detected gesture ('Up', 'Down', 'Left', 'Right', or 'Unknown').

#### `continuous_read_gesture(self, only_known_gestures=True, delay_ms=50, detection_threshold=50)`
Continuously reads gestures from the sensor.

- **Parameters:**
  - `only_known_gestures` (bool, optional): If `True`, only known gestures are returned. Default is `True`.
  - `delay_ms` (int, optional): The delay in milliseconds between each read. Default is 50 ms.
  - `detection_threshold` (int, optional): The minimum time in milliseconds between consecutive detections of the same gesture. Default is 50 ms.

- **Yields:**
  - `str`: The detected gesture ('Up', 'Down', 'Left', 'Right', or 'Unknown').

### ColorDetectionController Class
#### Methods
#### `__init__(self, i2c)`
Initializes the `ColorDetectionController` with the specified I2C interface.

- **Parameters:**
  - `i2c` (I2C): The I2C interface to communicate with the APDS-9960 sensor.

#### `read_color(self)`
Reads the current color from the sensor.

- **Returns:**
  - `tuple`: A tuple containing the RGB values and the color name.

#### `continuous_read_color(self, delay_ms=50, detection_threshold=50)`
Continuously reads colors from the sensor.

- **Parameters:**
  - `delay_ms` (int, optional): The delay in milliseconds between each read. Default is 50 ms.
  - `detection_threshold` (int, optional): The minimum time in milliseconds between consecutive detections of the same color. Default is 50 ms.

- **Yields:**
  - `tuple`: A tuple containing the RGB values and the color name.

### LightSensorController Class
#### Methods
#### `__init__(self, i2c)`
Initializes the `LightSensorController` with the specified I2C interface.

- **Parameters:**
  - `i2c` (I2C): The I2C interface to communicate with the APDS-9960 sensor.

#### `read_light(self)`
Reads the current light level from the sensor.

- **Returns:**
  - `float`: The normalized brightness value (0.0 to 1.0).

#### `continuous_read_light(self, delay_ms=50)`
Continuously reads light levels from the sensor.

- **Parameters:**
  - `delay_ms` (int, optional): The delay in milliseconds between each read. Default is 50 ms.

- **Yields:**
  - `float`: The normalized brightness value (0.0 to 1.0).

### ProximitySensorController Class
#### Methods
#### `__init__(self, i2c)`
Initializes the `ProximitySensorController` with the specified I2C interface.

- **Parameters:**
  - `i2c` (I2C): The I2C interface to communicate with the APDS-9960 sensor.

#### `read_proximity(self)`
Reads the current proximity value from the sensor.

- **Returns:**
  - `int`: The proximity value (0 to 255).

#### `continuous_read_proximity(self, delay_ms=50)`
Continuously reads proximity values from the sensor.

- **Parameters:**
  - `delay_ms` (int, optional): The delay in milliseconds between each read. Default is 50 ms.

- **Yields:**
  - `int`: The proximity value (0 to 255).

### ColorIdentifier Class
#### Methods
#### `__init__(self)`
Initializes the `ColorIdentifier` class.

#### `color_distance(self, color1, color2)`
Calculates the distance between two colors.

- **Parameters:**
  - `color1` (tuple): The first color as an (R, G, B) tuple.
  - `color2` (tuple): The second color as an (R, G, B) tuple.

- **Returns:**
  - `int`: The distance between the two colors.

#### `get_closest_color(self, r, g, b)`
Gets the closest predefined color to the given RGB values.

- **Parameters:**
  - `r` (int): The red component of the color.
  - `g` (int): The green component of the color.
  - `b` (int): The blue component of the color.

- **Returns:**
  - `tuple`: A tuple containing the closest color's RGB values and its name.

#### `get_hue(self, r, g, b)`
Determines the hue of the given RGB values.

- **Parameters:**
  - `r` (int): The red component of the color.
  - `g` (int): The green component of the color.
  - `b` (int): The blue component of the color.

- **Returns:**
  - `str`: The hue of the color.

#### `get_brightness_modifier(self, brightness)`
Determines the brightness modifier based on the brightness value.

- **Parameters:**
  - `brightness` (int): The brightness value.

- **Returns:**
  - `str`: The brightness modifier.

#### `get_color_name(self, r, g, b)`
Gets the name of the color based on the RGB values.

- **Parameters:**
  - `r` (int): The red component of the color.
  - `g` (int): The green component of the color.
  - `b` (int): The blue component of the color.

- **Returns:**
  - `str`: The name of the color.
