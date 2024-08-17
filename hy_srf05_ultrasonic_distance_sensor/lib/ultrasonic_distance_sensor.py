from machine import Pin, time_pulse_us
import utime

__SOUND_SPEED = 0.0343  # cm / us


class UltraSonicDistanceSensor:
    def __init__(self, trigger_pin, echo_pin, settle_time=2):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.trigger.low()
        if settle_time > 0:
            utime.sleep(settle_time)  # Allow time for sensor to settle

    def measure_distance(self, verbose=False):
        global __SOUND_SPEED
        # Trigger pulse
        self.trigger.value(1)
        utime.sleep_us(10)
        self.trigger.value(0)

        if verbose:
            print("Waiting for echo to go high")

        while not self.echo.value():
            pass

        if verbose:
            print("Waiting for echo to go low")

        echo_start = utime.ticks_us()
        while self.echo.value():
            pass
        echo_end = utime.ticks_us()

        echo_duration = utime.ticks_diff(echo_end, echo_start) // 2
        distance = echo_duration * __SOUND_SPEED

        if verbose:
            print("Echo duration:", echo_duration)

        return distance

    def average_distance(self, samples=3, delay_ms=60):
        total = 0
        for _ in range(samples):
            total += self.measure_distance(verbose=False)
            utime.sleep_ms(delay_ms)
        return total / samples
