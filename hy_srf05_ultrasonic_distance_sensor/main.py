import utime

from lib.ultrasonic_distance_sensor import UltraSonicDistanceSensor

# Initialize the sensor
print("Initializing UltraSonic Distance Sensor...")
sensor = UltraSonicDistanceSensor(trigger_pin=19, echo_pin=18)

# Main loop
delay = 0.3
while True:
    print("Measuring distance...")
    for i in range(10):
        distance = sensor.measure_distance()
        print(f"Distance: {distance:.2f} cm")
        utime.sleep(delay)

    print("Averaging distance...")
    for i in range(10):
        avg_distance = sensor.average_distance()
        print(f"Average Distance: {avg_distance:.2f} cm")
        utime.sleep(delay)

    utime.sleep(delay)
