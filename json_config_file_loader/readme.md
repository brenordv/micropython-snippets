# JSON Config File Loader
This project provides a simple configuration manager for loading and accessing configuration values from a JSON file.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- Raspberry Pi Pico

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### ConfigManager Class
### Methods

#### `__init__(self, config_file="appsettings.json")`
Initializes the `ConfigManager` instance.

- **Parameters:**
  - `config_file` (str): The path to the JSON configuration file.

#### `load_config(self)`
Loads the configuration from the JSON file.

#### `get_value(self, key, default_value=None)`
Retrieves a value from the configuration.

- **Parameters:**
  - `key` (str): The key of the configuration value.
  - `default_value` (any): The default value to return if the key is not found.

- **Returns:**
  - `any`: The value associated with the key, or the default value if the key is not found.

## Example Usage
```python
from lib.config_manager import ConfigManager

config_manager = ConfigManager()

values_to_get = [
    "this_file",
    "some_number",
    "some_string",
    "some_boolean",
    "some_array",
    "some_object"
]

for value in values_to_get:
    print(f"{value}: {config_manager.get_value(value)}")