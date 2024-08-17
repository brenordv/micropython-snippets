from machine import ADC, Pin
import utime


class SoilMoistureSensorController:
    def __init__(self, pin, max_value=57582, min_value=26054):
        self.soil_sensor = ADC(Pin(pin))

        # Initial Calibration
        self.max_value = max_value  # 100% Dry. No soil or water around.
        self.min_value = min_value  # 100% Wet. Dipped into a cup of water.

    def read_moisture(self):
        # Read the raw analog value
        raw_value = self.soil_sensor.read_u16()

        moisture_percentage = (self.max_value - raw_value) / (self.max_value - self.min_value) * 100
        moisture_percentage = max(0, min(100, moisture_percentage))  # Clamp value between 0 and 100

        return moisture_percentage, raw_value

    def calibrate(self, max_value=None, min_value=None):
        if max_value is not None:
            self.max_value = max_value
        if min_value is not None:
            self.min_value = min_value
