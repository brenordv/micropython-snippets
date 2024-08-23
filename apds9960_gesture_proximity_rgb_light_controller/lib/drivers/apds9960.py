# Based on: https://github.com/QuirkyCort/IoTy/blob/main/public/extensions/apds9960.py

import struct
import utime
from micropython import const

GAIN_1 = const(0)
GAIN_2 = const(1)
GAIN_4 = const(2)
GAIN_8 = const(3)

AGAIN_1 = const(0)
AGAIN_4 = const(1)
AGAIN_16 = const(2)
AGAIN_64 = const(3)

LED_100MA = const(0)
LED_50MA = const(1)
LED_25MA = const(2)
LED_12MA = const(3)

G_THRESHOLD = const(10)
G_SENSITIVITY = const(10)

RGBC_VALID = const(0x01)
ATIME_DEFAULT = const(219)  # 103ms integration time


class APDS9960:
    def __init__(self, i2c, addr=57):
        self.i2c = i2c
        self.addr = addr
        self.init_device()
        self.gesture = ''

    def _read(self, reg, size):
        return self.i2c.readfrom_mem(self.addr, reg, size)

    def _write(self, reg, data):
        return self.i2c.writeto_mem(self.addr, reg, data)

    def init_device(self):
        # pwr on, everything else off
        self._write(0x80, bytes([1]))

    # Gain from 0 to 3
    def enable_light_sensor(self, gain=AGAIN_1, atime=ATIME_DEFAULT):
        cfg = self._read(0x8F, 1)[0]
        cfg &= 0b11111100
        cfg |= (gain & 0b11)
        self._write(0x8F, bytes([cfg]))

        self._write(0x81, bytes([atime]))

        cfg = self._read(0x80, 1)[0]
        cfg |= 0b10
        self._write(0x80, bytes([cfg]))

    def disable_light_sensor(self):
        cfg = self._read(0x80, 1)[0]
        cfg &= 0b11111101
        self._write(0x80, bytes([cfg]))

    def read_light(self):
        data = self._read(0x94, 8)
        return struct.unpack('>HHHH', data)

    def enable_prox_sensor(self, gain=GAIN_1, led=LED_100MA):
        cfg = self._read(0x8F, 1)[0]
        cfg &= 0b00110011
        cfg |= (gain & 0b11) << 2
        cfg |= (led & 0b11) << 6
        self._write(0x8F, bytes([cfg]))

        cfg = self._read(0x80, 1)[0]
        cfg |= 0b100
        self._write(0x80, bytes([cfg]))

    def disable_prox_sensor(self):
        cfg = self._read(0x80, 1)[0]
        cfg &= 0b11111011
        self._write(0x80, bytes([cfg]))

    def read_prox(self):
        return self._read(0x9C, 1)[0]

    def enable_gesture_sensor(self, gain=GAIN_4, led=LED_100MA, prox_enter=40, prox_exit=30):
        cfg = 0b1
        cfg |= (led & 0b11) << 3
        cfg |= (gain & 0b11) << 5
        self._write(0xA3, bytes([cfg]))

        cfg = 0x40 # FIFO threshold 4, all detectors, 1st gesture end
        self._write(0xA2, bytes([cfg]))

        self._write(0xA0, bytes([prox_enter]))
        self._write(0xA1, bytes([prox_exit]))

        cfg = self._read(0x80, 1)[0]
        cfg |= 0b1000100 # enables prox as well
        self._write(0x80, bytes([cfg]))

    def disable_gesture_sensor(self):
        cfg = self._read(0x80, 1)[0]
        cfg &= 0b10111111
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
                if first == None:
                    first = d

        if last == None:
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

    def enable_rgb_sensor(self, gain=AGAIN_1, atime=ATIME_DEFAULT):
        # Enable ALS (Ambient Light Sensing)
        cfg = self._read(0x80, 1)[0]
        cfg |= 0b10  # Set AEN bit
        self._write(0x80, bytes([cfg]))

        # Set gain
        self.set_rgb_gain(gain)

        # Set integration time
        self.set_rgb_atime(atime)

    def set_rgb_gain(self, gain):
        cfg = self._read(0x8F, 1)[0]
        cfg &= 0b11111100
        cfg |= (gain & 0b11)
        self._write(0x8F, bytes([cfg]))

    def set_rgb_atime(self, atime):
        self._write(0x81, bytes([atime]))

    def auto_gain_rgb(self):
        gain = AGAIN_1
        atime = ATIME_DEFAULT

        while True:
            self.set_rgb_gain(gain)
            self.set_rgb_atime(atime)
            utime.sleep_ms(50)  # Wait for the new settings to take effect

            _, _, _, clear = self.read_rgb()

            if clear < 100:  # Too dark
                if gain < AGAIN_64:
                    gain += 1
                elif atime > 1:
                    atime -= 1
                else:
                    break  # Can't increase sensitivity further
            elif clear > 60000:  # Too bright
                if atime < 255:
                    atime += 1
                elif gain > AGAIN_1:
                    gain -= 1
                else:
                    break  # Can't decrease sensitivity further
            else:
                break  # Good range

        return gain, atime

    def disable_rgb_sensor(self):
        cfg = self._read(0x80, 1)[0]
        cfg &= 0b11111101  # Clear AEN bit
        self._write(0x80, bytes([cfg]))

    def rgb_data_valid(self):
        status = self._read(0x93, 1)[0]
        return (status & RGBC_VALID) == RGBC_VALID

    def read_rgb(self):
        while not self.rgb_data_valid():
            utime.sleep_ms(5)

        data = self._read(0x94, 8)
        clear, red, green, blue = struct.unpack('>HHHH', data)
        return red, green, blue, clear

    def read_rgb_normalized(self):
        red, green, blue, clear = self.read_rgb()
        if clear > 0:
            red = min(255, (red * 255) // clear)
            green = min(255, (green * 255) // clear)
            blue = min(255, (blue * 255) // clear)
        else:
            red, green, blue = 0, 0, 0
        return red, green, blue
