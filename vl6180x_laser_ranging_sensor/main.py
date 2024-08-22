from lib.laser_ranging_sensor_controller import LaserRangingSensorController

# Example usage:
sda_pin = 20
scl_pin = 21
sensor = LaserRangingSensorController(sda_pin, scl_pin)

for distance, in_range, gesture in sensor.continuous_get_distance_and_gesture():
    print(f"Distance: {distance} mm, in range: {in_range}, gesture: {gesture}")
