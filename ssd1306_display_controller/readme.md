# SSD1306 Micropython Display Controller
This is a wrapper around the ssd1306 driver to make things a bit easier to use.

## Installation
Just copy the `lib` folder to your board.

## Demo
![Controller demo](.demo/display_demo.gif)

## Hardware
- Raspberry Pi Pico
- SSD1306 - IZOKEE 0.96" I2C IIC 12864 128X64 Pixel OLED LCD Display

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### SSD1306 Pinout
![ssd1306_pinout.png](.assets%2Fssd1306_pinout.png)

### SSD1306 Datasheet
[SSD1306.pdf](.assets%2FSSD1306.pdf)

## DisplayController Class
### Methods
#### `__init__(self, scl_pin, sda_pin, width=128, height=64, frequency=200000, progress_bar_char="|", verbose=False)`
Initializes the `DisplayController` with the specified I2C pins, display dimensions, frequency, progress bar character, and verbosity.

- **Parameters:**
  - `scl_pin` (int): The pin number for the I2C clock.
  - `sda_pin` (int): The pin number for the I2C data.
  - `width` (int, optional): The width of the display. Default is 128.
  - `height` (int, optional): The height of the display. Default is 64.
  - `frequency` (int, optional): The I2C frequency. Default is 200000.
  - `progress_bar_char` (str, optional): The character used for the progress bar. Default is "|".
  - `verbose` (bool, optional): If `True`, enables verbose logging. Default is `False`.

#### `clear(self, flush=False)`
Clears the display.

- **Parameters:**
  - `flush` (bool, optional): If `True`, immediately updates the display. Default is `False`.

#### `write(self, text, line_num, print_log=True)`
Writes text to a specific line on the display.

- **Parameters:**
  - `text` (str): The text to display.
  - `line_num` (int): The line number to write the text to (1-based index).
  - `print_log` (bool, optional): If `True`, logs the text being written. Default is `True`.

#### `progress_bar(self, value, line_num=None, max_value=1.0, print_log=True)`
Displays a progress bar on the specified line.

- **Parameters:**
  - `value` (float): The current progress value.
  - `line_num` (int, optional): The line number to display the progress bar. Default is the last line.
  - `max_value` (float, optional): The maximum value for the progress bar. Default is 1.0.
  - `print_log` (bool, optional): If `True`, logs the progress bar being displayed. Default is `True`.

#### `draw_raccoon(self)`
Draws a raccoon ASCII art on the display.

#### `_log(self, message)`
Logs a message if verbose mode is enabled.

- **Parameters:**
  - `message` (str): The message to log.

#### `_validate_text(self, text, line_num)`
Validates the text and line number.

- **Parameters:**
  - `text` (str): The text to validate.
  - `line_num` (int): The line number to validate.

- **Returns:**
  - `bool`: `True` if the text and line number are valid, otherwise `False`.

#### `_get_progress_bar(self, percent_value)`
Generates a progress bar string based on the percentage value.

- **Parameters:**
  - `percent_value` (float): The percentage value for the progress bar.

- **Returns:**
  - `str`: The progress bar string.
