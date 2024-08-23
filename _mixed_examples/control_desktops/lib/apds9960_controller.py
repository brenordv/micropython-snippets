import time

from lib.drivers.apds9960 import APDS9960


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

        if self.last_gesture_detection_time is None or detection_threshold is None or detection_threshold <= 0:
            return True

        return (detection_time - self.last_gesture_detection_time) > detection_threshold

    def read_gesture(self):
        gesture = self.sensor.read_gesture()
        self.gesture = self.driver_gesture_map.get(gesture, self.unknown_gesture)
        return self.gesture

    def continuous_read_gesture(self, only_known_gestures = True, delay_ms=50, detection_threshold=50):
        while True:
            gesture = self.read_gesture()
            gesture_time = time.monotonic_ns() // 1_000_000  # Convert to milliseconds
            if self._should_return_gesture(gesture, gesture_time, detection_threshold, only_known_gestures):
                self.last_gesture = gesture
                self.last_gesture_detection_time = gesture_time
                yield gesture

            time.sleep(delay_ms / 1000)
