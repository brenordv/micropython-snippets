import time

from lib.gas_detection_sensor import GasDetectionSensor


sensor = GasDetectionSensor(26)

while True:
    value = sensor.read()

    print("PPM: {:.2f}, Normalized: {:.3f}".format(
        value["ppm"],
        value["normalized"])
    )

    time.sleep(0.05)
