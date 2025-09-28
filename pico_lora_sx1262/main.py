# MicroPython LoRa "modem" for Raspberry Pi Pico W + Waveshare Pico-LoRa-SX1262
# - Plain text over USB serial
# - Non-blocking LoRa TX/RX with callback
# - Framed messages and TX-done notifications
#
# Host protocol:
#   Send: <LoRa-Message-Package>your text here</LoRa-Message-Package>
#   Receive (from LoRa): <LoRa-Message-Package>peer text here</LoRa-Message-Package>
#   TX done: <Lora-System-Info-Tx-Done>{"bytes":N,"toa_ms":X,"elapsed_ms":Y,"status":Z}</Lora-System-Info-Tx-Done>

import sys, uselect, utime, ujson
from machine import Pin, SPI
from lib.sx1262 import SX1262

# ---------- Configuration ----------
# Choose your regional frequency (MHz) and LoRa params
LORA_FREQ_MHZ   = 915.0      # e.g., 915.0 for US915, 868.0 for EU868
LORA_BW_KHZ     = 125.0
LORA_SF         = 7          # 5..12
LORA_CR         = 8          # coding rate denominator (5..8) -> CR = 4/(CR)
LORA_POWER_DBM  = 14
LORA_SYNC_WORD  = 0x12       # private networks

# Tag constants
OPEN_TAG  = "<LoRa-Message-Package>"
CLOSE_TAG = "</LoRa-Message-Package>"
TXI_OPEN  = "<Lora-System-Info-Tx-Done>"
TXI_CLOSE = "</Lora-System-Info-Tx-Done>"

# Waveshare Pico-LoRa-SX1262 HAT pinout on Pico (SPI1 + control lines)
# SPI1: SCK=GP10, MOSI=GP11, MISO=GP12
# CS/NSS=GP3, DIO1/IRQ=GP20, RST=GP15, BUSY=GP2
# (Confirmed mapping for this HAT; use hardware SPI1.)  See: RadioLib discussion.
SPI_ID = 1
PIN_SCK  = 10
PIN_MOSI = 11
PIN_MISO = 12
PIN_CS   = 3
PIN_IRQ  = 20
PIN_RST  = 15
PIN_BUSY = 2

# ---------- Globals ----------
poll = uselect.poll()
poll.register(sys.stdin, uselect.POLLIN)

serial_buf = ""             # accumulate incoming USB serial
tx_queue = []               # queue of pending bytes to send over LoRa
tx_busy = False             # true while a TX is in progress
last_tx = {"len": 0, "t0": 0, "status": None}

# ---------- LoRa setup ----------
spi = SPI(
    SPI_ID,
    baudrate=1_000_000,
    polarity=0, phase=0,
    sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI), miso=Pin(PIN_MISO)
)

lora = SX1262(
    spi_bus=SPI_ID, clk=PIN_SCK, mosi=PIN_MOSI, miso=PIN_MISO,
    cs=PIN_CS, irq=PIN_IRQ, rst=PIN_RST, gpio=PIN_BUSY
)

def _print_line(s: str):
    # Single place for printing back to USB (line-oriented)
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

def _emit_tx_done():
    # Called after TX_DONE interrupt has fired
    toa_ms = 0
    try:
        toa_ms = int(lora.getTimeOnAir(last_tx["len"]))  # library-provided estimate
    except Exception:
        pass
    elapsed = 0
    try:
        elapsed = utime.ticks_diff(utime.ticks_ms(), last_tx["t0"])
    except Exception:
        pass
    info = {
        "bytes": last_tx["len"],
        "toa_ms": toa_ms,
        "elapsed_ms": elapsed,
        "status": last_tx["status"],
    }
    _print_line(f"{TXI_OPEN}{ujson.dumps(info)}{TXI_CLOSE}")

def _kick_tx_queue():
    global tx_busy, last_tx
    if tx_busy or not tx_queue:
        return
    payload = tx_queue.pop(0)
    # Record start time and length for TX-done report
    last_tx["len"] = len(payload)
    last_tx["t0"] = utime.ticks_ms()
    try:
        ret = lora.send(payload)  # non-blocking (we enabled callbacks below)
        # Driver returns (payload_len, status)
        if isinstance(ret, tuple) and len(ret) >= 2:
            last_tx["status"] = ret[1]
        else:
            last_tx["status"] = ret
        tx_busy = True
    except Exception as e:
        last_tx["status"] = f"error:{e}"
        tx_busy = False
        _emit_tx_done()  # still emit a line so host isn't left hanging

def lora_irq_handler(events):
    # Called by the driver in non-blocking mode
    global tx_busy
    try:
        # RX complete?
        if events & SX1262.RX_DONE:
            data, _status = lora.recv()  # returns (payload_bytes, status)
            try:
                text = data.decode("utf-8")
            except Exception:
                text = data.decode("utf-8", "replace")
            _print_line(f"{OPEN_TAG}{text}{CLOSE_TAG}")

        # TX complete?
        if events & SX1262.TX_DONE:
            tx_busy = False
            _emit_tx_done()
            _kick_tx_queue()
    except Exception as _:
        # Swallow IRQ exceptions; keep system running
        pass

# Configure radio (non-blocking) and enable callback
lora.begin(
    freq=LORA_FREQ_MHZ, bw=LORA_BW_KHZ, sf=LORA_SF, cr=LORA_CR,
    syncWord=LORA_SYNC_WORD, power=LORA_POWER_DBM,
    currentLimit=60.0, preambleLength=8,
    implicit=False, implicitLen=0xFF, crcOn=True,
    txIq=False, rxIq=False, tcxoVoltage=1.6,
    useRegulatorLDO=False, blocking=False  # non-blocking mode
)
lora.setBlockingCallback(False, lora_irq_handler)

# ---------- Main loop ----------
def process_usb():
    """Non-blocking read of USB serial, extract framed packages, push to TX queue."""
    global serial_buf
    if not poll.poll(0):
        return
    ch = sys.stdin.read(1)
    if not ch:
        return
    serial_buf += ch

    # Extract all complete frames in the buffer (handles back-to-back messages)
    while True:
        si = serial_buf.find(OPEN_TAG)
        if si < 0:
            # Optional: drop buffer if it grows too big with junk
            if len(serial_buf) > 4096:
                serial_buf = ""
            return
        ei = serial_buf.find(CLOSE_TAG, si + len(OPEN_TAG))
        if ei < 0:
            # not complete yet
            # Trim any leading junk before OPEN_TAG
            if si > 0:
                serial_buf = serial_buf[si:]
            return

        # Extract payload and consume the frame
        payload_text = serial_buf[si + len(OPEN_TAG):ei]
        serial_buf = serial_buf[ei + len(CLOSE_TAG):]

        # Enqueue for TX (encode to bytes; UTF-8)
        tx_queue.append(payload_text.encode("utf-8"))
        _kick_tx_queue()

def main():
    # Idle loop; LoRa events arrive via IRQ callback
    print("Starting...")
    while True:
        process_usb()
        utime.sleep_ms(5)

if __name__ == "__main__":
    main()
