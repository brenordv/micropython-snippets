import serial, time, json, re

PORT = "/dev/ttyACM0"  # or COMx on Windows
ser = serial.Serial(PORT, 115200, timeout=0.1)

def send(msg: str):
    pkt = f"<LoRa-Message-Package>{msg}</LoRa-Message-Package>\n"
    ser.write(pkt.encode("utf-8"))

rx_tag = re.compile(r"<LoRa-Message-Package>(.*?)</LoRa-Message-Package>")
tx_tag = re.compile(r"<Lora-System-Info-Tx-Done>(.*?)</Lora-System-Info-Tx-Done>")

send("hello from host")
t0 = time.time()
while time.time() - t0 < 10:
    line = ser.readline().decode(errors="replace").strip()
    if not line:
        continue
    if m := rx_tag.search(line):
        print("LoRa RX:", m.group(1))
    if m := tx_tag.search(line):
        print("TX DONE:", json.loads(m.group(1)))
