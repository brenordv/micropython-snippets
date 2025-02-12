# Board Monitor
This project is a simple monitor for system parameters of a board, including memory usage, internal temperature, CPU frequency, and uptime.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- Raspberry Pi Pico

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### BoardMonitor Class
### Methods

#### `__init__(self)`
Initializes the `BoardMonitor` instance.

- **Attributes:**
  - `start_time` (int): The start time for uptime calculations.
  - `temp_sensor` (machine.ADC): An ADC instance for reading the internal temperature sensor.

#### `get_memory_info(self)`
Retrieves memory usage details of the board.

- **Returns:**
  - `dict`: A dictionary containing free, used, and total memory in bytes.

#### `get_internal_temperature(self)`
Reads and converts the internal temperature sensor value.

- **Returns:**
  - `float`: The estimated internal temperature in degrees Celsius.

#### `get_cpu_frequency(self)`
Retrieves the current CPU frequency of the board.

- **Returns:**
  - `int`: The CPU frequency in Hz.

#### `get_uptime(self)`
Calculates the system uptime since the board was powered on or reset.

- **Returns:**
  - `float`: Uptime in seconds.

#### `get_status(self)`
Collects and returns system status information.

- **Returns:**
  - `dict`: A dictionary containing memory usage, internal temperature, CPU frequency, and uptime.