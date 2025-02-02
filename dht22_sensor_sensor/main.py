from lib.temp_and_humidity_sensor import TempAndHumiditySensor

sensor = TempAndHumiditySensor(9)

print("Reading sensor values...")
for success, temperature, humidity, timestamp in sensor.continuous_measurement():
    if not success:
        print('Failed to read sensor')
        continue

    print(f'Temperature: {temperature}°C, Humidity: {humidity}% / Timestamp: {timestamp}')
