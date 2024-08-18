from lib.ir_motion_sensor_controller import InfraredMotionSensorController

sensor = InfraredMotionSensorController(sensor_pin=18)

detected = 0
for motion_detected in sensor.continuous_motion_detection():
    if motion_detected:
        detected += 1
        print(f"Motion detected! - {detected:010d}", end="\r")
