import utime

from lib.drivers.apds9960 import APDS9960
from lib.color_identifier import ColorIdentifier
from lib.drivers.apds9960 import AGAIN_16


class GestureDetectionController:
    def __init__(self, i2c):
        self.sensor = APDS9960(i2c)
        self.sensor.enable_gesture_sensor()
        self.gesture = ''
        self.driver_gesture_map = {
            "u": "Up",
            "d": "Down",
            "l": "Left",
            "r": "Right"
        }
        self.unknown_gesture = 'Unknown'
        self.last_gesture = None
        self.last_gesture_detection_time = None

    def _should_return_gesture(self, gesture, detection_time, detection_threshold, only_known_gestures):
        if only_known_gestures and gesture == self.unknown_gesture:
            return False

        if self.last_gesture == gesture:
            return False

        if self.last_gesture_detection_time is None or detection_threshold is None or detection_threshold <= 0:
            return True

        return utime.ticks_diff(detection_time, self.last_gesture_detection_time) > detection_threshold

    def read_gesture(self):
        gesture = self.sensor.read_gesture()
        self.gesture = self.driver_gesture_map.get(gesture, self.unknown_gesture)
        return self.gesture

    def continuous_read_gesture(self, only_known_gestures = True, delay_ms=50, detection_threshold=50):
        while True:
            gesture = self.read_gesture()
            gesture_time = utime.ticks_ms()
            if self._should_return_gesture(gesture, gesture_time, detection_threshold, only_known_gestures):
                self.last_gesture = gesture
                self.last_gesture_detection_time = gesture_time
                yield gesture

            utime.sleep_ms(delay_ms)


class ColorDetectionController:
    def __init__(self, i2c):
        self.sensor = APDS9960(i2c)
        self.sensor.enable_rgb_sensor()
        self.color = None
        self.color_name = None
        self.last_color = None
        self.last_color_detection_time = None
        self.color_identifier = ColorIdentifier()

    def _should_return_color(self, color, detection_time, detection_threshold):
        if self.last_color == color:
            return False

        if self.last_color_detection_time is None or detection_threshold is None or detection_threshold <= 0:
            return True

        return utime.ticks_diff(detection_time, self.last_color_detection_time) > detection_threshold

    def read_color(self):
        color = self.sensor.read_rgb_normalized()
        self.color = color
        self.color_name = self.color_identifier.get_color_name(*color)
        return color, self.color_name

    def continuous_read_color(self, delay_ms=50, detection_threshold=50):
        while True:
            color, color_name = self.read_color()
            color_time = utime.ticks_ms()

            if self._should_return_color(color, color_time, detection_threshold):
                self.last_color = color
                self.last_color_detection_time = color_time
                yield color, color_name

            utime.sleep_ms(delay_ms)


class LightSensorController:
    def __init__(self, i2c):
        self.sensor = APDS9960(i2c)
        self.sensor.enable_light_sensor(gain=AGAIN_16)
        self.light = None
        # The maximum possible value is 65535, but shining a flashlight directly at the sensor can cause it to read a value of 64552.
        # You might want to calibrate this value based on your specific use case.
        self.max_clear_value = 64552

    def read_light(self):
        (red, green, blue, clear) = self.sensor.read_light()

        # Normalize the 'clear' value.
        normalized_brightness = min(clear / self.max_clear_value, 1.0)

        self.light = normalized_brightness
        return normalized_brightness

    def continuous_read_light(self, delay_ms=50):
        while True:
            light = self.read_light()
            yield light
            utime.sleep_ms(delay_ms)


class ProximitySensorController:
    def __init__(self, i2c):
        self.sensor = APDS9960(i2c)
        self.sensor.enable_prox_sensor()
        self.proximity = None

    def read_proximity(self):
        # 0 - No proximity detected
        # 255 - Almost touching the sensor
        proximity = self.sensor.read_prox()
        self.proximity = proximity
        return proximity

    def continuous_read_proximity(self, delay_ms=50):
        while True:
            proximity = self.read_proximity()
            yield proximity
            utime.sleep_ms(delay_ms)
