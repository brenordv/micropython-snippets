from lib.temperature_controller import TemperatureSensor

sensor = TemperatureSensor(28)

print("Reading sensor values...")
for success, temperature, timestamp in sensor.continuous_measurement():
    if not success:
        print('[Main] Failed to read sensor')
        continue

    print(f'Temperature: {temperature}°C / Timestamp: {timestamp}')
