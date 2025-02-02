from lib.laser_ranging_sensor_sensor import LaserRangingSensorSensor

# Example usage:
sda_pin = 20
scl_pin = 21
sensor = LaserRangingSensorSensor(sda_pin, scl_pin)

for distance, in_range in sensor.continuous_get_distance():
    print(f"Distance: {distance} mm, in range: {in_range}")
