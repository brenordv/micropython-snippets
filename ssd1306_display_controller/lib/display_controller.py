from machine import Pin, I2C

from lib.driver import ssd1306


class DisplayController:
    def __init__(self, scl_pin, sda_pin, width=128, height=64, frequency=200000, progress_bar_char="|", verbose=False):
        self.verbose = verbose

        self._log("Initializing I2C")
        i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=frequency)

        self._log("Initializing display")
        self.display = ssd1306.SSD1306_I2C(width, height, i2c)
        self.progress_bar_char = progress_bar_char
        self.width = width
        self.height = height
        self.line_height = 10
        self.line_size = 16  # "0123456789ABCDEF"
        self.max_lines = 6
        self.max_chars = self.line_size * self.max_lines
        self._log(f"Display initialized with width={width}, height={height}, line_height={self.line_height}, max lines={self.max_lines}, max chars={self.max_chars}")
        self._log("Display controller initialized")

    def _get_progress_bar(self, percent_value):
        display_progress = int(self.line_size * percent_value)
        return self.progress_bar_char * display_progress

    def _log(self, message):
        if not self.verbose:
            return
        print(f"[DISPLAY] {message}")

    def _validate_text(self, text, line_num,):
        if line_num > self.max_lines:
            self._log(f"[ERROR] Line number {line_num} exceeds max lines")
            return False

        if line_num == 0:
            self._log("[ERROR] Line number starts at 1")
            return False

        if len(text) > self.line_size:
            self._log(f"[WARN] Text will be truncated because it exceeds line size")

        return True

    def clear(self, flush=False):
        self.display.fill(0)
        if flush:
            self._log("Clearing and flushing display")
            self.display.show()
        else:
            self._log("Clearing display")

    def write(self, text, line_num, align="left", print_log=True):
        if not self._validate_text(text, line_num):
            return

        line = line_num - 1
        x_position = 0

        if align == "right":
            x_position = self.width - len(text) * 8  # Assuming 8 pixels per character
        elif align == "center":
            x_position = (self.width - len(text) * 8) // 2  # Center the text

        self.display.fill_rect(0, self.line_height * line, self.width, self.line_height, 0)
        self.display.text(text, x_position, self.line_height * line)

        if print_log:
            self._log(f"[LINE {line_num}] {text}")

        self.display.show()

    def progress_bar(self, value, line_num=None, max_value=1.0, print_log=True):
        if line_num is None:
            line_num = self.max_lines

        progress_bar = self._get_progress_bar(value / max_value)
        if not self._validate_text(progress_bar, line_num):
            return

        self.write(progress_bar, line_num, print_log=print_log)

    def draw_raccoon(self):
        self.clear()
        self.write("hey, look...", 1)
        self.write("...a raccoon! :D", 2)
        self.write("     /\_/\  ", 3)
        self.write("    ( o.o ) ", 4)
        self.write("     > ^ <  ", 5)
        self.display.show()
        self._log("Raccoon drawn")
