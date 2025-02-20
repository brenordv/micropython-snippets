import time

from lib.photoresistor import Photoresistor

p = Photoresistor(26)


while True:
    val = p.read()
    print(f"Light value: {val}")
    time.sleep(0.1)
