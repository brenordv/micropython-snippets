from machine import ADC, Pin
import utime

soil_sensor = ADC(Pin(26))  # ADC0 on GPIO 26


def read_soil_moisture():
    # Read the raw analog value
    raw_value = soil_sensor.read_u16()

    # Values calibrated for the sensor.
    max_value = 57582  # 100% Dry. No soil or water around.
    min_value = 26054  # 100% Wet. Dipped into a cup of water.

    moisture_percentage = (max_value - raw_value) / (max_value - min_value) * 100
    moisture_percentage = max(0, min(100, moisture_percentage))  # Clamp value between 0 and 100

    return moisture_percentage, raw_value


# Main program
print("Sensor warming up...")
utime.sleep(2)  # Give the sensor 2 seconds to stabilize after power-on
show_raw = False

while True:
    moisture, raw_value = read_soil_moisture()

    if show_raw:
        print(f"Sensor value: {raw_value}")
    else:
        print(f"Soil Moisture: {moisture:.2f}%")
    utime.sleep(0.1)  # Wait for 100ms before reading again
