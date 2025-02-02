from machine import ADC, Pin
import math


class GasDetectionSensor:
    def __init__(self, pin, rl_value=20.0, r0=10.0, m=-0.38, b=1.33, voltage_ref=3.3, adc_max=65535,err_return_value=0):
        """
        Initialize the gas detection sensor with the ADC pin and calibration values.

        :param pin: The number of the pin where the sensor is connected.
        :param rl_value: The load resistance value in kOhms (default: 20.0).
        :param r0: The sensor resistance in clean air in kOhms (default: 10.0).
        :param m: The slope from the log-log calibration curve (default: -0.38).
        :param b: The intercept from the log-log calibration curve (default: 1.33).
        :param voltage_ref: The reference voltage of the ADC (default: 3.3).
        :param err_return_value: The value to return in case of an error (default: 0).
        :param adc_max: The maximum value of the ADC (default: 65535).
        """
        self.rl_value = rl_value
        self.r0 = r0
        self.m = m
        self.b = b
        self.voltage_ref = voltage_ref
        self.err_return_value = err_return_value
        self.adc_max = adc_max
        self.adc = ADC(Pin(pin))

    def _convert_raw_to_voltage(self, raw_value):
        """
        Convert the raw ADC value to a voltage based on the ADC resolution and reference voltage.
        """
        return (raw_value / self.adc_max) * self.voltage_ref

    def _calculate_sensor_resistance(self, voltage):
        """
        Calculate the sensor resistance (Rs) from the measured voltage.
        Formula: Rs = RL * (Vcc/Vout - 1)
        """
        if voltage <= 0:
            return self.err_return_value
        return self.rl_value * (self.voltage_ref / voltage - 1)

    def read_raw_value(self):
        """
        Read the raw ADC value (0 to 65535) from the sensor.
        """
        return self.adc.read_u16()

    def read_ppm(self, raw_value=None):
        """
        Convert the raw ADC value to an estimated gas concentration in PPM using the sensor's calibration curve.
        1. Convert raw value to voltage.
        2. Calculate sensor resistance.
        3. Use the log-log calibration: log10(ppm) = (log10(Rs/R0) - b) / m.
        """
        raw_value = self.read_raw_value() if raw_value is None else raw_value
        voltage = self._convert_raw_to_voltage(raw_value)
        rs = self._calculate_sensor_resistance(voltage)
        if rs is None or rs <= 0:
            return self.err_return_value
        ratio = rs / self.r0
        try:
            # Apply the calibration equation
            ppm = math.pow(10, (math.log10(ratio) - self.b) / self.m)
            return ppm
        except ValueError:
            return self.err_return_value

    def read_normalized(self, raw_value=None):
        """
        Convert the raw ADC value to a normalized value between 0.0 and 1.0.
        """
        raw_value = self.read_raw_value() if raw_value is None else raw_value
        return raw_value / self.adc_max

    def read(self):
        """
        Read the raw ADC value, PPM value, and normalized value.
        """
        raw_value = self.read_raw_value()
        ppm_value = self.read_ppm(raw_value)
        normalized_value = self.read_normalized(raw_value)
        return {
            "raw": raw_value,
            "ppm": ppm_value if ppm_value else 0,
            "normalized": normalized_value
        }
