from machine import ADC, Pin
import math


class SmokeDetectorSensor:
    def __init__(self, pin, rl_value=5.0, r0=None, m=-0.45, b=1.4, voltage_ref=3.3, adc_max=65535, err_return_value=0):
        """
        Initialize the MQ-2 gas detection sensor with recommended calibration values.

        :param pin: The number of the ADC pin where the sensor's analog output is connected.
        :param rl_value: Load resistance in kΩ (default: 5.0 for typical MQ-2 modules).
        :param r0: Sensor resistance in clean air (default: None, must be calibrated).
        :param m: Slope of the calibration curve (default: -0.45).
        :param b: Intercept of the calibration curve (default: 1.4).
        :param voltage_ref: ADC reference voltage (default: 3.3V).
        :param adc_max: Maximum ADC value (default: 65535 for 16-bit ADC).
        :param err_return_value: Value returned on error (default: 0).
        """
        self.rl_value = rl_value
        self.r0 = r0
        self.m = m
        self.b = b
        self.voltage_ref = voltage_ref
        self.adc_max = adc_max
        self.err_return_value = err_return_value
        self.adc = ADC(Pin(pin))

    def _convert_raw_to_voltage(self, raw_value):
        """
        Convert the raw ADC value to a voltage.
        """
        return (raw_value / self.adc_max) * self.voltage_ref

    def _calculate_sensor_resistance(self, voltage):
        """
        Calculate the sensor resistance (Rs) from the measured voltage using the voltage divider formula:
        Rs = RL * (Vcc/Vout - 1)
        """
        if voltage <= 0:
            return self.err_return_value
        return self.rl_value * (self.voltage_ref / voltage - 1)

    def read_raw_value(self):
        """
        Read the raw ADC value (0 to 65535) from the sensor.
        """
        return self.adc.read_u16()

    def read_resistance(self, raw_value=None):
        """
        Convert the raw ADC value to sensor resistance using the voltage divider formula.
        Useful when wanting to calibrate the sensor in clean air.
        """
        raw_value = self.read_raw_value() if raw_value is None else raw_value
        voltage = self._convert_raw_to_voltage(raw_value)
        return self._calculate_sensor_resistance(voltage)

    def read_ppm(self, raw_value=None):
        """
        Convert the raw ADC value to an estimated gas concentration in PPM.

        The process involves:
          1. Converting the raw value to a voltage.
          2. Calculating the sensor resistance (Rs).
          3. Using the log-log calibration curve:
             log10(ppm) = (log10(Rs/R0) - b) / m.
        """
        raw_value = self.read_raw_value() if raw_value is None else raw_value
        rs = self.read_resistance(raw_value)
        if rs is None or rs <= 0:
            return self.err_return_value
        ratio = rs / self.r0
        try:
            ppm = math.pow(10, (math.log10(ratio) - self.b) / self.m)
            return ppm
        except ValueError:
            return self.err_return_value

    def read_normalized(self, raw_value=None):
        """
        Convert the raw ADC value to a normalized value between 0.0 and 1.0,
        where 1.0 represents the maximum ADC value.
        """
        raw_value = self.read_raw_value() if raw_value is None else raw_value
        return raw_value / self.adc_max

    def read(self):
        """
        Read the sensor and return a dictionary with:
          - The raw ADC value.
          - The estimated gas concentration in PPM.
          - The normalized ADC value.
        """
        raw_value = self.read_raw_value()
        ppm_value = self.read_ppm(raw_value)
        normalized_value = self.read_normalized(raw_value)
        return {
            "raw": raw_value,
            "ppm": ppm_value if ppm_value else 0,
            "normalized": normalized_value
        }
