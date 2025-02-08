# Unique ID Library
A simple library to retrieve the unique ID of a MicroPython board.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- Any MicroPython-compatible board

## Methods

### `get_unique_id()`
Retrieves the unique ID of the board in both hexadecimal and integer formats.

- **Returns:**
  - `tuple`: A tuple containing the unique ID as a hex string and as an integer.

## Usage

Below is a quick example demonstrating how to use the `get_unique_id` function:

```python
from lib.unique_id import get_unique_id

unique_id_hex, unique_id_int = get_unique_id()
print("This board's unique ID as an integer:")
print(unique_id_int)

print("This board's unique ID as a hex string:")
print(unique_id_hex)
```