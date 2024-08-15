import utime

from lib.SoilMoistureSensorController import SoilMoistureSensorController

sensor_controller = SoilMoistureSensorController(pin=26)

# Main program
print("Sensor warming up...")
utime.sleep(2)  # Give the sensor 2 seconds to stabilize after power-on
show_raw = False

while True:
    moisture, raw_value = sensor_controller.read_moisture()

    if show_raw:
        print(f"Sensor value: {raw_value}")
    else:
        print(f"Soil Moisture: {moisture:.2f}%")
    utime.sleep(0.1)  # Wait for 100ms before reading again
