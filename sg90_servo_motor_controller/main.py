from lib.sg90_servo_controller import Sg90ServoController

# Initialize the servo on GPIO pin 15
servo = Sg90ServoController(22)

print("Swiping the servo from 0 to 180 degrees")
print("Press Ctrl+C to stop")
for current_angle in servo.sweep_infinite(0, 180):
    print(f"Current angle: {current_angle}")
