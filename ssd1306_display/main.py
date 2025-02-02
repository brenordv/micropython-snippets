import time

from lib.display_controller import DisplayController


display = DisplayController(scl_pin=1, sda_pin=0, verbose=True)

display.clear(flush=True)
display.draw_raccoon()
time.sleep(2)

display.clear(flush=True)

display.write("How are you?", line_num=3)
time.sleep(0.3)
display.write("Hi!", line_num=1)
time.sleep(0.3)
display.write("Hello!", line_num=2)
time.sleep(0.3)
display.write("Can't complain!", line_num=5)
time.sleep(0.3)
display.write("Good, and you?", line_num=4)
time.sleep(0.3)
display.write("Ok, bye!", line_num=6)
time.sleep(0.3)

display.clear(flush=True)

display.write("Working...", line_num=1)
time.sleep(0.15)

for i in range(0, 101):
    display.progress_bar(i / 100, line_num=2)
    time.sleep(0.001)

display.clear(flush=True)

time.sleep(0.3)
display.write("Alright!", line_num=1)
time.sleep(0.3)
display.write("All done!", line_num=3, align="right")
time.sleep(0.3)
display.write("Bye!", line_num=6, align="center")
