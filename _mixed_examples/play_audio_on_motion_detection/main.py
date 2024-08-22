import utime
from lib.ir_motion_sensor_controller import InfraredMotionSensorController
from lib.audio_player import AudioPlayer

print("Initializing HC-SR501 IR Motion Sensor...")
sensor = InfraredMotionSensorController(sensor_pin=18)

print("Initializing YX5200 Mini MP3 Player...")
player = AudioPlayer(uart=0, tx_pin=16, rx_pin=17, busy_pin=22, initial_volume=30)

print("Waiting 10 seconds for you to get out of the way before start working...")
utime.sleep(10)

print("Starting motion detection...")
detected = 0
checks = 0
for motion_detected in sensor.continuous_motion_detection():
    checks += 1

    if checks % 100 == 0:
        print(f"Checks: {checks:010d} - Detected: {detected:010d}", end="\r")

    if not motion_detected:
        continue

    detected += 1
    print(f"Motion detected! - {detected:010d}", end="\r")
    player.play_sync(1)
