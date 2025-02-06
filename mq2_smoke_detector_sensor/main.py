import time

from lib.smoke_detector_sensor import SmokeDetectorSensor


smoke_detector = SmokeDetectorSensor(pin=27)

while True:
    sensor_values = smoke_detector.read()
    print("PPM: {:.2f}, Normalized: {:.3f}".format(
        sensor_values["ppm"],
        sensor_values["normalized"]
    ))
    time.sleep(0.05)
