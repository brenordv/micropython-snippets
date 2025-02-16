# Error Log Manager
This project provides a simple error logging manager for storing and managing error logs in JSON format.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- Raspberry Pi Pico

### ErrorLogManager Class
### Methods

#### `__init__(self, log_folder)`
Initializes the `ErrorLogManager` instance.

- **Parameters:**
  - `log_folder` (str): The path to the folder where log files will be stored.

#### `_create_log_folder_if_not_exists(self)`
Creates the log folder if it does not exist.

#### `_folder_exists(self, folder_path)`
Checks if a folder exists.

- **Parameters:**
  - `folder_path` (str): The path of the folder to check.

- **Returns:**
  - `bool`: True if the folder exists, False otherwise.

#### `log_error(self, error_message, error_object=None)`
Logs an error message and an optional error object to a JSON log file with a timestamp.

- **Parameters:**
  - `error_message` (str): A description of the error.
  - `error_object` (Exception, optional): The exception object, if applicable.

#### `list_logs(self)`
Lists all log files in the log folder.

- **Returns:**
  - `list`: A list of log filenames.

#### `read_log(self, log_filename)`
Reads a specific log file and returns the JSON content.

- **Parameters:**
  - `log_filename` (str): The name of the log file to read.

- **Returns:**
  - `dict`: The contents of the log file as a dictionary.

#### `delete_log(self, log_filename)`
Deletes a specific log file by name.

- **Parameters:**
  - `log_filename` (str): The name of the log file to delete.

## Example Usage
```python
from lib.error_log_manager import ErrorLogManager

log_manager = ErrorLogManager("logs")

try:
    1 / 0  # Simulating an error
except Exception as e:
    log_manager.log_error("Division by zero error", e)

# List logs
logs = log_manager.list_logs()
print("Logs available:", logs)

# Read first log if exists
if logs:
    log_content = log_manager.read_log(logs[0])
    print("First log content:", log_content)

# Optional: Delete the first log file
if logs:
    log_manager.delete_log(logs[0])
    print("Deleted log:", logs[0])
```

