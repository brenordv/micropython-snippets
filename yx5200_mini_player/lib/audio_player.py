from machine import UART, Pin
import utime


class AudioPlayer:
    def __init__(self, uart, tx_pin, rx_pin, busy_pin, baud_rate=9600):
        self.uart = UART(uart, baudrate=baud_rate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.busy_pin = Pin(busy_pin, Pin.IN)
        print(f"AudioPlayer initialized with UART {uart}, TX: {tx_pin}, RX: {rx_pin}, BUSY: {busy_pin}")

    def _send_command(self, cmd, param1=0, param2=0):
        command = bytes([0x7E, 0xFF, 0x06, cmd, 0x00, param1, param2, 0xEF])
        self.uart.write(command)
        print(f"Sent command: {[hex(b) for b in command]}")
        utime.sleep_ms(100)
        self._read_response()

    def _read_response(self):
        if self.uart.any():
            response = self.uart.read()
            print(f"Received response: {[hex(b) for b in response]}")
        else:
            print("No response received")

    def play(self, track_number):
        print(f"Attempting to play track number: {track_number}")
        self._send_command(0x03, 0, track_number)

    def set_volume(self, volume):
        print(f"Setting volume to: {volume}")
        self._send_command(0x06, 0x00, min(max(volume, 0), 100))

    def is_playing(self):
        return self.busy_pin.value() == 0