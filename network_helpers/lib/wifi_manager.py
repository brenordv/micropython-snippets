import network
import time


class WifiManager:
    def __init__(self, ssid, password, connection_timeout=30, max_connection_retries=3):
        self.ssid = ssid
        self.password = password
        self.connection_timeout = connection_timeout
        self.max_connection_retries = max_connection_retries
        self.current_connection_attempt = 1
        self.wlan = None

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        start_time = time.time()
        while not self.wlan.isconnected() and time.time() - start_time < self.connection_timeout:
            time.sleep(1)

        if self.wlan.isconnected():
            ip = self.wlan.ifconfig()[0]
            return ip

        if self.current_connection_attempt <= self.max_connection_retries:
            self.current_connection_attempt += 1
            self.turn_wifi_off()
            return self.connect()

    def turn_wifi_off(self):
        if self.wlan is None:
            return False

        try:
            print(f"Current WiFi status: {self.wlan.status()} | is_connected: {self.wlan.isconnected()}")
            # https://github.com/micropython/micropython/blob/31d7ab327b0da4fe7747aba5590a542b88caa123/drivers/cyw43/cyw43_ctrl.c#L127
            self.wlan.deinit()

        except Exception as e:
            print("Error turning WiFi off")
            print(e)
            self.wlan.active(False)

        return True
