from machine import Pin, PWM
import utime


class Sg90ServoController:
    def __init__(self, pin_number, initial_angle=90, frequency=50, min_duty=1640, max_duty=8190, current_angle=90):
        self.servo = PWM(Pin(pin_number))
        self.servo.freq(frequency)  # 50Hz frequency for SG90
        self._min_duty = min_duty  # Duty cycle for 0 degrees (0.5ms pulse)
        self._max_duty = max_duty  # Duty cycle for 180 degrees (2.5ms pulse)
        self.current_angle = current_angle
        self.set_angle(initial_angle)  # Initialize at 90 degrees

    def set_to_min(self):
        self.set_angle(0)

    def set_to_max(self):
        self.set_angle(180)

    def set_to_mid(self):
        self.set_angle(90)

    def set_angle(self, angle):
        """
        Set the servo to a specific angle (0-180 degrees)
        """
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        duty = int(self._min_duty + (self._max_duty - self._min_duty) * angle / 180)
        self.servo.duty_u16(duty)
        self.current_angle = angle
        utime.sleep_ms(100)  # Allow time for the servo to move

    def get_angle(self):
        """
        Get the current angle of the servo
        """
        return self.current_angle

    def sweep_infinite(self, start_angle, end_angle, step=4, delay_ms=0):
        """
        Generator function to continuously sweep the servo from start_angle to end_angle
        """
        while True:
            for angle in range(start_angle, end_angle + 1, step):
                self.set_angle(angle)
                if delay_ms > 0:
                    utime.sleep_ms(delay_ms)
                yield angle

            for angle in range(end_angle, start_angle - 1, -step):
                self.set_angle(angle)
                if delay_ms > 0:
                    utime.sleep_ms(delay_ms)
                yield angle

    def sweep_one_shot(self, start_angle, end_angle, step=4, delay_ms=0):
        """
        Sweep the servo from start_angle to end_angle
        """
        if start_angle < end_angle:
            range_func = range(start_angle, end_angle + 1, step)
        else:
            range_func = range(start_angle, end_angle - 1, -step)

        for angle in range_func:
            self.set_angle(angle)
            if delay_ms > 0:
                utime.sleep_ms(delay_ms)

    def detach(self):
        """
        Stop sending PWM signals to the servo
        """
        self.servo.deinit()
