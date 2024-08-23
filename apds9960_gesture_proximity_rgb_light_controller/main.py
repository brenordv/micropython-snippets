from machine import I2C, Pin


from lib.apds9960_controller import GestureDetectionController, ColorDetectionController, LightSensorController, \
    ProximitySensorController

# Set up I2C
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

# Initialize the controllers
mode = 4
gesture_controller = GestureDetectionController(i2c)
color_controller = ColorDetectionController(i2c)
light_controller = LightSensorController(i2c)
proximity_controller = ProximitySensorController(i2c)

if mode == 1:
    # Testing gesture detection
    print("Starting gesture detection")
    count = 0
    for gesture in gesture_controller.continuous_read_gesture(only_known_gestures=True):
        count += 1
        print(f"[{count:010d}] Gesture detected: {gesture}")

elif mode == 2:
    # Testing color detection
    print("Starting color detection")
    count = 0
    for color, color_name in color_controller.continuous_read_color():
        count += 1
        print(f"[{count:010d}] Color detected: {color} / {color_name}")

elif mode == 3:
    # Testing light detection
    print("Starting light detection")
    count = 0
    for light in light_controller.continuous_read_light():
        count += 1
        print(f"[{count:010d}] Light detected: {light}                          ")

elif mode == 3.1:
    # Testing light detection
    print("Starting light detection")
    count = 0
    max_light = 0
    for light in light_controller.continuous_read_light():
        if light > max_light:
            max_light = light
        print(f"Light detected: {max_light}")

elif mode == 4:
    # Testing proximity detection
    print("Starting proximity detection")
    print("0 - No proximity detected")
    print("255 - Almost touching the sensor")
    count = 0
    for proximity in proximity_controller.continuous_read_proximity():
        count += 1
        print(f"[{count:010d}] Proximity detected: {proximity}")
