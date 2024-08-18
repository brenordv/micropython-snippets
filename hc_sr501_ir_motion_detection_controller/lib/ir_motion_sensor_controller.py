from machine import Pin
import utime

class InfraredMotionSensorController:
    def __init__(self, sensor_pin):
        self.sensor_pin = Pin(sensor_pin, Pin.IN)

    def is_motion_detected(self):
        return self.sensor_pin.value() == 1

    def continuous_motion_detection(self, delay_ms=50):
        while True:
            yield self.is_motion_detected()
            utime.sleep_ms(delay_ms)
