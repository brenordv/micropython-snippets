import dht
from machine import Pin
import utime


class Dht22Error(BaseException):
    def __init__(self, message):
        super().__init__(f"Failed to read sensor: {message}")


class TempAndHumidityController:
    def __init__(self, pin, temp_offset=0, humidity_offset=0):
        self.sensor = dht.DHT22(Pin(pin))
        self.temp_offset = temp_offset
        self.humidity_offset = humidity_offset
        self.temperature = None
        self.humidity = None
        self.last_error_message = None

    def measure(self):
        try:
            self.sensor.measure()
            self.temperature = self.sensor.temperature() + self.temp_offset
            self.humidity = self.sensor.humidity() + self.humidity_offset
            return True
        except OSError as e:
            self.last_error_message = str(e)
            return False

    def get_temperature(self):
        if self.temperature is not None:
            return self.temperature
        else:
            return None

    def get_humidity(self):
        if self.humidity is not None:
            return self.humidity
        else:
            return None

    def get_last_error_message(self):
        return self.last_error_message

    def set_temp_calibration(self, offset):
        self.temp_offset = offset

    def set_humidity_calibration(self, offset):
        self.humidity_offset = offset

    def get_readings(self):
        if self.measure():
            return {
                "timestamp": utime.ticks_ms(),
                "temperature": self.temperature,
                "humidity": self.humidity
            }
        else:
            return None

    def continuous_measurement(self, max_consecutive_failures=10, delay_ms=1000):
        consecutive_failures = 0

        while True:
            measurement = self.get_readings()
            if measurement is not None:
                consecutive_failures = 0
                yield True, measurement['temperature'], measurement['humidity'], measurement['timestamp']
            else:
                consecutive_failures += 1
                yield False, None, None, None

            if consecutive_failures >= max_consecutive_failures:
                raise Dht22Error(f'Failed to read sensor for {max_consecutive_failures} consecutive times. Error: {self.last_error_message}')

            utime.sleep_ms(delay_ms)
