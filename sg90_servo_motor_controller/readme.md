# SG90 Micro Servo Motor Controller
Simple class that controls a single SG90 micro servo motor.
There is nothing special about this class, but it's always useful to have this kind of code snippet ready to use.

To use this, copy the `lib` folder to your project.

## Hardware
- SG90 micro servo motor
- Raspberry Pi Pico

## SG90 Micro Servo Pinout
![Servo_pinout-1024x546.png](.assets%2FServo_pinout-1024x546.png)

## Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

## SG90 Datasheet
[SG90-datasheet.pdf](.assets%2FSG90-datasheet.pdf)

### Sg90ServoController Class
### Methods

#### `__init__(self, pin_number, initial_angle=90, frequency=50, min_duty=1640, max_duty=8190, current_angle=90)`
Initializes the `Sg90ServoController` with the specified pin number, initial angle, frequency, minimum and maximum duty cycles, and current angle.

- **Parameters:**
  - `pin_number` (int): The GPIO pin number to which the servo is connected.
  - `initial_angle` (int, optional): The initial angle of the servo. Default is 90 degrees.
  - `frequency` (int, optional): The PWM frequency. Default is 50 Hz.
  - `min_duty` (int, optional): The minimum duty cycle for 0 degrees. Default is 1640.
  - `max_duty` (int, optional): The maximum duty cycle for 180 degrees. Default is 8190.
  - `current_angle` (int, optional): The current angle of the servo. Default is 90 degrees.

#### `set_to_min(self)`
Sets the servo to the minimum angle (0 degrees).

#### `set_to_max(self)`
Sets the servo to the maximum angle (180 degrees).

#### `set_to_mid(self)`
Sets the servo to the middle angle (90 degrees).

#### `set_angle(self, angle)`
Sets the servo to a specific angle (0-180 degrees).

- **Parameters:**
  - `angle` (int): The angle to set the servo to.

#### `get_angle(self)`
Gets the current angle of the servo.

- **Returns:**
  - `int`: The current angle of the servo.

#### `sweep_infinite(self, start_angle, end_angle, step=4, delay_ms=0)`
Generator function to continuously sweep the servo from `start_angle` to `end_angle`.

- **Parameters:**
  - `start_angle` (int): The starting angle of the sweep.
  - `end_angle` (int): The ending angle of the sweep.
  - `step` (int, optional): The step size for each increment. Default is 4 degrees.
  - `delay_ms` (int, optional): The delay in milliseconds between each step. Default is 0 ms.

- **Yields:**
  - `int`: The current angle of the servo during the sweep.

#### `sweep_one_shot(self, start_angle, end_angle, step=4, delay_ms=0)`
Sweeps the servo from `start_angle` to `end_angle` once.

- **Parameters:**
  - `start_angle` (int): The starting angle of the sweep.
  - `end_angle` (int): The ending angle of the sweep.
  - `step` (int, optional): The step size for each increment. Default is 4 degrees.
  - `delay_ms` (int, optional): The delay in milliseconds between each step. Default is 0 ms.

#### `detach(self)`
Stops sending PWM signals to the servo.
