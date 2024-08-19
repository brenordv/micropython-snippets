import utime
from machine import Pin

from lib.ds18x20_exceptions import Ds18x20Error
import lib.drivers.onewire as onewire
import lib.drivers.ds18x20 as ds18x20


class TemperatureController:
    def __init__(self, pin, temp_offset=0):
        self.pin = Pin(pin)
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(self.pin))
        self.roms = self.ds_sensor.scan()
        print("Found DS18X20 devices:", self.roms)
        self.temp_offset = temp_offset
        self.temperature = None
        self.last_error_message = None

    def measure(self):
        try:
            self.ds_sensor.convert_temp()
            # DS18X20 requires a delay after converting temperature
            utime.sleep_ms(750)
            if self.roms:
                self.temperature = self.ds_sensor.read_temp(self.roms[0]) + self.temp_offset
                return True
            else:
                self.last_error_message = "No DS18X20 device found"
                return False
        except Exception as e:
            self.last_error_message = str(e)
            return False

    def get_temperature(self):
        return self.temperature

    def set_temp_calibration(self, offset):
        self.temp_offset = offset

    def get_readings(self):
        if self.measure():
            return {
                "timestamp": utime.time(),
                "temperature": self.temperature
            }
        else:
            return None

    def get_last_error(self):
        return self.last_error_message

    def continuous_measurement(self, max_consecutive_failures=10, delay_ms=1000):
        consecutive_failures = 0

        while True:
            measurement = self.get_readings()
            if measurement is not None:
                consecutive_failures = 0
                yield True, measurement["temperature"], measurement["timestamp"]
            else:
                consecutive_failures += 1
                yield False, None, None

            if consecutive_failures >= max_consecutive_failures:
                raise Ds18x20Error(f"Failed to read sensor for {max_consecutive_failures} consecutive times. Error: {self.last_error_message}")

            utime.sleep_ms(delay_ms)

    def measure_with_retry(self, retries=3, delay_ms=1000):
        for _ in range(retries):
            if self.measure():
                return self.get_readings()
            utime.sleep_ms(delay_ms)
        return None
