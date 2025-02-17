import time

LOG_LEVEL = {
    "TRACE": 0,
    "DEBUG": 1,
    "INFO": 2,
    "WARN": 3,
    "ERROR": 4,
    "CRITICAL": 5
}


class TelemetryLoggerHttp:
    """
    TelemetryLogger buffers log entries and flushes them to an API endpoint, via HTTP post requests.
    """

    def __init__(self, http_client, device_seq_id, endpoint="/data-points/telemetry", batch_size=5, flush_interval=10, instant_flush=False):
        """
        :param http_client: Instance of HttpClient to send logs.
        :param device_seq_id: Unique identifier for the device.
        :param endpoint: API endpoint path for log posts.
        :param batch_size: Number of logs before an automatic flush.
        :param flush_interval: Maximum time (seconds) to wait before flushing.
        :param instant_flush: If True, flush logs immediately after each log entry.
        """
        self.http_client = http_client
        self.endpoint = endpoint
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.log_buffer = []
        self.last_flush_time = time.time()
        self.device_seq_id = device_seq_id
        self.instant_flush = instant_flush

    def _create_log_entry(self, timestamp, level, message, **kwargs):
        """Create a log entry dictionary."""

        log_level = LOG_LEVEL.get(level, 0)
        log_entry = {
            "device_seq_id": self.device_seq_id,
            "log_level": log_level,
            "timestamp": timestamp,
            "message": message,
            "extras": kwargs
        }
        return log_entry

    def update_device_seq_id(self, device_seq_id):
        """Update the device sequence ID."""
        self.device_seq_id = device_seq_id

    def log(self, timestamp, level, message, **kwargs):
        """
        Add a log entry to the buffer.

        :param timestamp: String ISO8601 timestamp.
        :param level: Log level string (e.g., 'INFO', 'ERROR').
        :param message: Message string.
        :param kwargs: Any additional context information.
        """
        level = level.upper().strip() if level else "INFO"

        log_entry = self._create_log_entry(timestamp, level, message, **kwargs)

        self.log_buffer.append(log_entry)

        if len(kwargs) == 0:
            print(f"[{level}] {message}")
        else:
            print(f"[{level}] {message} | {kwargs}")

        if self.instant_flush or \
                len(self.log_buffer) >= self.batch_size or \
                (time.time() - self.last_flush_time) >= self.flush_interval:
            self.flush()

    def flush(self):
        """Send buffered logs to the API."""
        if not self.log_buffer:
            return  # Nothing to flush.

        try:
            for msg in self.log_buffer:
                success, response = self.http_client.post(self.endpoint, json=msg)
                if not success:
                    print(f"Failed to send log. Resulting status: {response['status_code']}")
        except Exception as e:
            print("Failed to send logs:", e)
        finally:
            # Clear the buffer and reset the flush timer.
            self.log_buffer = []
            self.last_flush_time = time.time()
