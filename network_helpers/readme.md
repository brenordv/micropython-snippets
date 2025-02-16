# Network Helpers
This project provides a set of helper libraries for network-related tasks, including
- WiFi management: connecting to a WiFi network and turning off the WiFi connection.
- NTP synchronization and local time retrieval (in UTC): synchronizing the local time with an NTP server and retrieving the local time in ISO8601 format.
- HTTP client: performing HTTP GET and POST requests, using retries, timeouts, and garbage collection to allow for long running operations.
- Telemetry Client: logging telemetry data to an HTTP endpoint, with support for batching and flushing.

## Installation
Just copy the `lib` folder to your board.

## Hardware
- Raspberry Pi Pico

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### WifiManager Class
### Methods

#### `__init__(self, ssid, password, connection_timeout=30, max_connection_retries=3)`
Initializes the `WifiManager` instance.

- **Parameters:**
  - `ssid` (str): The SSID of the WiFi network.
  - `password` (str): The password of the WiFi network.
  - `connection_timeout` (int): Timeout for each connection attempt (in seconds).
  - `max_connection_retries` (int): Maximum number of connection retries.

#### `connect(self)`
Connects to the WiFi network.

- **Returns:**
  - `str`: The IP address if connected successfully.

#### `turn_wifi_off(self)`
Turns off the WiFi connection.

- **Returns:**
  - `bool`: True if WiFi was turned off successfully, False otherwise.

### NtpHelper Class
### Methods

#### `__init__(self, host=None, resync_period=3600)`
Initializes the `NtpHelper` instance.

- **Parameters:**
  - `host` (str): Optional NTP server host.
  - `resync_period` (int): Period for resynchronization (in seconds).

#### `sync(self)`
Synchronizes the local time with the NTP server.

#### `get_local_time(self)`
Retrieves the local time in ISO8601 format.

- **Returns:**
  - `str`: The local time as a string.

### HttpClient Class
### Methods

#### `__init__(self, base_url="", timeout=5, retries=3)`
Initializes the `HttpClient` instance.

- **Parameters:**
  - `base_url` (str): Optional base URL to prefix to all requests.
  - `timeout` (int): Timeout for each request (in seconds).
  - `retries` (int): Number of retry attempts for failed requests.

#### `get(self, path, params=None, **kwargs)`
Performs an HTTP GET request.

- **Parameters:**
  - `path` (str): URL path or full URL.
  - `params` (dict): Dictionary of query parameters to append to the URL.
  - `kwargs` (dict): Additional arguments for the request.

- **Returns:**
  - `tuple`: A tuple containing a boolean indicating success and a dictionary with the response content and status code.

#### `post(self, path, data=None, json=None, **kwargs)`
Performs an HTTP POST request.

- **Parameters:**
  - `path` (str): URL path or full URL.
  - `data` (str): Data to send in the body (for form-encoded posts, etc.).
  - `json` (dict): A JSON-serializable object to send as JSON.
  - `kwargs` (dict): Additional arguments for the request.

- **Returns:**
  - `tuple`: A tuple containing a boolean indicating success and a dictionary with the response content and status code.

### TelemetryLoggerHttp Class
### Methods

#### `__init__(self, http_client, device_seq_id, endpoint="/data-points/telemetry", batch_size=5, flush_interval=10, instant_flush=False)`
Initializes the `TelemetryLoggerHttp` instance.

- **Parameters:**
  - `http_client` (HttpClient): Instance of `HttpClient` to send logs.
  - `device_seq_id` (str): Unique identifier for the device.
  - `endpoint` (str): API endpoint path for log posts.
  - `batch_size` (int): Number of logs before an automatic flush.
  - `flush_interval` (int): Maximum time (seconds) to wait before flushing.
  - `instant_flush` (bool): If True, flush logs immediately after each log entry.

#### `log(self, timestamp, level, message, **kwargs)`
Adds a log entry to the buffer.

- **Parameters:**
  - `timestamp` (str): String ISO8601 timestamp.
  - `level` (str): Log level string (e.g., 'INFO', 'ERROR').
  - `message` (str): Message string.
  - `kwargs` (dict): Any additional context information.

#### `flush(self)`
Sends buffered logs to the API.