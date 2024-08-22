from machine import Pin, I2C
import utime

from lib.drivers.vl6180x import Vl6180X


class LaserRangingSensorController:
    def __init__(self, sda_pin, scl_pin, gesture_threshold=10, i2c_freq=400000):
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=i2c_freq)
        self.address = 0x29  # Default I2C address for VL6180X
        self.sensor = Vl6180X(self.i2c, self.address)
        self.max_value = 50
        self.gesture_threshold = gesture_threshold

    def get_distance(self):
        distance = self.sensor.range()
        in_range = distance <= self.max_value

        return distance, in_range

    def continuous_get_distance(self, delay_ms=50):
        while True:
            yield self.get_distance()
            utime.sleep_ms(delay_ms)
