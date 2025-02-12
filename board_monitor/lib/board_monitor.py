import gc
import machine
import utime


class BoardMonitor:
    """
    A MicroPython class for monitoring system parameters of a board,
    including memory usage, internal temperature, CPU frequency, and uptime.
    """

    def __init__(self):
        """
        Initializes the BoardMonitor instance.

        - Records the start time for uptime calculations.
        - Sets up an ADC instance for reading the internal temperature sensor.
        """
        self.start_time = utime.ticks_ms()
        self.temp_sensor = machine.ADC(4)  # Internal temperature sensor (channel 4)

    def get_memory_info(self):
        """
        Retrieves memory usage details of the board.

        Returns:
            dict: A dictionary containing free, used, and total memory in bytes.
        """
        free_mem = gc.mem_free()
        used_mem = gc.mem_alloc()
        total_mem = free_mem + used_mem
        return {
            "free": free_mem,
            "used": used_mem,
            "total": total_mem
        }

    def get_internal_temperature(self):
        """
        Reads and converts the internal temperature sensor value.

        Returns:
            float: The estimated internal temperature in degrees Celsius.
        """
        reading = self.temp_sensor.read_u16()
        voltage = reading * 3.3 / 65535  # Convert ADC reading to voltage
        temperature = 27 - (voltage - 0.706) / 0.001721  # Convert voltage to temperature
        return temperature

    def get_cpu_frequency(self):
        """
        Retrieves the current CPU frequency of the board.

        Returns:
            int: The CPU frequency in Hz.
        """
        return machine.freq()

    def get_uptime(self):
        """
        Calculates the system uptime since the board was powered on or reset.

        Returns:
            float: Uptime in seconds.
        """
        uptime_ms = utime.ticks_diff(utime.ticks_ms(), self.start_time)
        return uptime_ms / 1000  # Convert milliseconds to seconds

    def get_status(self):
        """
        Collects and returns system status information.

        Returns:
            dict: A dictionary containing memory usage, internal temperature,
                  CPU frequency, and uptime.
        """
        return {
            "memory": self.get_memory_info(),
            "internal_temperature_celsius": self.get_internal_temperature(),
            "cpu_frequency_hz": self.get_cpu_frequency(),
            "uptime_seconds": self.get_uptime()
        }
