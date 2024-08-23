import time
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

GAIN_1 = 0
GAIN_2 = 1
GAIN_4 = 2
GAIN_8 = 3

AGAIN_1 = 0
AGAIN_4 = 1
AGAIN_16 = 2
AGAIN_64 = 3

LED_100MA = 0
LED_50MA = 1
LED_25MA = 2
LED_12MA = 3

G_THRESHOLD = 10
G_SENSITIVITY = 10

RGBC_VALID = 0x01
ATIME_DEFAULT = 219  # 103ms integration time


class APDS9960:
    def __init__(self, i2c, addr=0x39):
        self.i2c_device = I2CDevice(i2c, addr)
        self.addr = addr
        self.init_device()
        self.gesture = ''

    def _read(self, reg, size):
        result = bytearray(size)
        with self.i2c_device as i2c:
            i2c.write_then_readinto(bytes([reg]), result)
        return result

    def _write(self, reg, data):
        with self.i2c_device as i2c:
            i2c.write(bytes([reg]) + data)

    def init_device(self):
        # Power on, everything else off
        self._write(0x80, bytes([1]))

    def enable_gesture_sensor(self, gain=GAIN_4, led=LED_100MA, prox_enter=40, prox_exit=30):
        cfg = 0b1
        cfg |= (led & 0b11) << 3
        cfg |= (gain & 0b11) << 5
        self._write(0xA3, bytes([cfg]))

        cfg = 0x40  # FIFO threshold 4, all detectors, 1st gesture end
        self._write(0xA2, bytes([cfg]))

        self._write(0xA0, bytes([prox_enter]))
        self._write(0xA1, bytes([prox_exit]))

        cfg = self._read(0x80, 1)[0]
        cfg |= 0b1000100  # enables prox as well
        self._write(0x80, bytes([cfg]))

    def _gesture_available(self):
        return (self._read(0xAF, 1)[0] & 0b1) == 0b1

    def read_gesture(self):
        if not self._gesture_available():
            self.gesture = ''
            return ''

        first = None
        last = None

        fifo_lvl = self._read(0xAE, 1)[0]
        for _ in range(fifo_lvl):
            d = self._read(0xFC, 4)
            if d[0] > G_THRESHOLD and d[1] > G_THRESHOLD and d[2] > G_THRESHOLD and d[3] > G_THRESHOLD:
                last = d
                if first is None:
                    first = d

        if last is None:
            self.gesture = ''
            return ''

        ud_ratio_first = ((first[0] - first[1]) * 100) // (first[0] + first[1])
        lr_ratio_first = ((first[2] - first[3]) * 100) // (first[2] + first[3])
        ud_ratio_last = ((last[0] - last[1]) * 100) // (last[0] + last[1])
        lr_ratio_last = ((last[2] - last[3]) * 100) // (last[2] + last[3])

        ud_delta = ud_ratio_last - ud_ratio_first
        lr_delta = lr_ratio_last - lr_ratio_first

        if abs(ud_delta) < G_SENSITIVITY and abs(lr_delta) < G_SENSITIVITY:
            self.gesture = ''
            return ''

        if abs(ud_delta) > abs(lr_delta):
            if ud_delta > 0:
                self.gesture = 'u'
            else:
                self.gesture = 'd'
        else:
            if lr_delta > 0:
                self.gesture = 'l'
            else:
                self.gesture = 'r'

        return self.gesture

    def get_gesture(self):
        return self.gesture
