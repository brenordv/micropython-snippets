import dht
from machine import Pin
import utime
import math


class Dht22Error(BaseException):
    def __init__(self, message):
        super().__init__(f"Failed to read sensor: {message}")


class TempAndHumiditySensor:
    def __init__(self, pin, temp_calibration=None, humidity_calibration=None):
        self.sensor = dht.DHT22(Pin(pin))
        self.temp_calibration = temp_calibration
        self.humidity_calibration = humidity_calibration
        self.use_temp_calibration = self.temp_calibration is not None and all(key in self.temp_calibration for key in ['scale', 'offset'])
        self.use_humidity_calibration = self.humidity_calibration is not None and all(key in self.humidity_calibration for key in ['scale', 'offset'])
        self.temperature = None
        self.humidity = None
        self.feels_like = None
        self.last_error_message = None

    def _calculate_feels_like(self, temp_c, current_humidity) -> float:
        """
        Calculate the apparent (feels-like) temperature using Heat Index for warm conditions
        and Humidex for moderate conditions.

        :param temp_c: Temperature in Celsius
        :param current_humidity: Relative humidity in %
        :return: Feels-like temperature in Celsius
        """

        # If temperature is below 10°C, return actual temperature
        if temp_c < 10:
            return temp_c

            # Convert Celsius to Fahrenheit for Heat Index calculation
        temp_f = (temp_c * 9 / 5) + 32

        # Heat Index Formula (only for high temperatures >26°C)
        if temp_c > 26:
            c1 = -42.379
            c2 = 2.04901523
            c3 = 10.14333127
            c4 = -0.22475541
            c5 = -6.83783 * (10 ** -3)
            c6 = -5.481717 * (10 ** -2)
            c7 = 1.22874 * (10 ** -3)
            c8 = 8.5282 * (10 ** -4)
            c9 = -1.99 * (10 ** -6)

            HI_f = (c1 + (c2 * temp_f) + (c3 * current_humidity) + (c4 * temp_f * current_humidity) +
                    (c5 * temp_f ** 2) + (c6 * current_humidity ** 2) + (c7 * temp_f ** 2 * current_humidity) +
                    (c8 * temp_f * current_humidity ** 2) + (c9 * temp_f ** 2 * current_humidity ** 2))

            # Convert Heat Index back to Celsius
            HI_c = (HI_f - 32) * 5 / 9
            return round(HI_c, 2)

        # Humidex formula (for moderate temperatures)
        dew_point = (243.12 * (math.log(current_humidity / 100.0) + ((17.62 * temp_c) / (243.12 + temp_c)))) / \
                    (17.62 - math.log(current_humidity / 100.0) - ((17.62 * temp_c) / (243.12 + temp_c)))

        humidex = temp_c + (5 / 9) * (6.112 * math.exp((17.62 * dew_point) / (243.12 + dew_point)) - 10)
        return humidex

    def measure(self):
        try:
            self.sensor.measure()

            if self.use_temp_calibration:
                self.temperature = (self.sensor.temperature() * self.temp_calibration["scale"]) + self.temp_calibration["offset"]
            else:
                self.temperature = self.sensor.temperature()

            if self.use_humidity_calibration:
                self.humidity = (self.sensor.humidity() * self.humidity_calibration["scale"]) + self.humidity_calibration["offset"]
            else:
                self.humidity = self.sensor.humidity()

            self.feels_like = self._calculate_feels_like(self.temperature, self.humidity)

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
                "humidity": self.humidity,
                "feels_like": self.feels_like
            }
        else:
            return None

    def continuous_measurement(self, max_consecutive_failures=10, delay_ms=1000):
        consecutive_failures = 0

        while True:
            measurement = self.get_readings()
            if measurement is not None:
                consecutive_failures = 0
                yield True, measurement['temperature'], measurement['humidity'], measurement["feels_like"], measurement['timestamp']
            else:
                consecutive_failures += 1
                yield False, None, None, None, None

            if consecutive_failures >= max_consecutive_failures:
                raise Dht22Error(f'Failed to read sensor for {max_consecutive_failures} consecutive times. Error: {self.last_error_message}')

            utime.sleep_ms(delay_ms)
