from machine import ADC

class Photoresistor:
    def __init__(self, adc_pin, volt=3.3):
        """
        Initializes the Photoresistor instance with an ADC pin.
        :param adc_pin: The ADC pin number where the photoresistor is connected.
        """
        self.adc = ADC(adc_pin)
        self.volt = volt

    def read(self):
        value = self.adc.read_u16()
        return value * self.volt / 65535
