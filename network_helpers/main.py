from lib.wifi_manager import WifiManager
from lib.ntp_helper import NtpHelper
from lib.telemetry_logger import TelemetryLoggerHttp
from lib.http_client import HttpClient

ntp_host = "use your own or leave it empty/null"
ssid = "use your own"
password = "use your own"
api_base_url = "use your own"

wifi_manager = WifiManager(ssid=ssid, password=password)

ip = wifi_manager.connect()
print(f"Connected to WiFi: {ip}")

ntp = NtpHelper(host=ntp_host)
print(f"Local time: {ntp.get_local_time()}")

http_client = HttpClient(base_url=api_base_url)

telemetry = TelemetryLoggerHttp(http_client, device_seq_id="1", instant_flush=True)

telemetry.log(timestamp=ntp.get_local_time(), level="info", message="Hello from Pi Pico!")

for i in range(100):
    telemetry.log(timestamp=ntp.get_local_time(), level="info", message=f"Counting: {i}", ip=ip)
