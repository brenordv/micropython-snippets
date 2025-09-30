import sys, uselect, utime, ujson
from machine import Pin, SPI
from sx1262 import SX1262


# Choose your regional frequency (MHz) and LoRa params
LORA_FREQ_MHZ_US   = 915.0      # e.g., 915.0 for US915, 868.0 for EU868
LORA_FREQ_MHZ_EU   = 868.0      # e.g., 915.0 for US915, 868.0 for EU868
LORA_BW_KHZ     = 125.0
LORA_SF         = 7          # 5..12
LORA_CR         = 8          # coding rate denominator (5..8) -> CR = 4/(CR)
LORA_POWER_DBM  = 14
LORA_SYNC_WORD  = 0x12       # private networks

# Waveshare Pico-LoRa-SX1262 HAT pinout on Pico (SPI1 + control lines)
# Not making those configurable because it is a hat, so we don't have a choice.
# SPI1: SCK=GP10, MOSI=GP11, MISO=GP12
# CS/NSS=GP3, DIO1/IRQ=GP20, RST=GP15, BUSY=GP2
SPI_ID = 1
PIN_SCK  = 10
PIN_MOSI = 11
PIN_MISO = 12
PIN_CS   = 3
PIN_IRQ  = 20
PIN_RST  = 15
PIN_BUSY = 2

LORA_OUTGOING_MSG_TAG = "LoRa-Message-Package"
LORA_RECEIVED_MSG_NOTIFY_TAG = "Lora-System-Info-Tx-Done"


class LoRaModem:
    def __init__(self, outgoing_msg_tag = None, incoming_msg_tag = None, use_us_freq=True):

        txi_tag = incoming_msg_tag if incoming_msg_tag is not None else LORA_RECEIVED_MSG_NOTIFY_TAG
        self._txi_open = f"<{txi_tag}>"
        self._txi_close = f"</{txi_tag}>"

        out_tag = outgoing_msg_tag if outgoing_msg_tag is not None else LORA_OUTGOING_MSG_TAG
        self._open_tag = f"<{out_tag}>"
        self._close_tag = f"</{out_tag}>"

        self.poll = uselect.poll()
        self.poll.register(sys.stdin, uselect.POLLIN)

        # accumulate incoming USB serial
        self.serial_buf = ""

        # queue of pending bytes to send over LoRa
        self.tx_queue = []

        # true while a TX is in progress
        self.tx_busy = False
        self.last_tx = {"len": 0, "t0": 0, "status": None}

        self.spi = SPI(
            SPI_ID,
            baudrate=1_000_000,
            polarity=0, phase=0,
            sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI), miso=Pin(PIN_MISO)
        )

        self.lora = SX1262(
            spi_bus=SPI_ID, clk=PIN_SCK, mosi=PIN_MOSI, miso=PIN_MISO,
            cs=PIN_CS, irq=PIN_IRQ, rst=PIN_RST, gpio=PIN_BUSY
        )

        # Configure radio (non-blocking) and enable callback
        self.lora.begin(
            freq=LORA_FREQ_MHZ_US if use_us_freq else LORA_FREQ_MHZ_EU,
            bw=LORA_BW_KHZ,
            sf=LORA_SF,
            cr=LORA_CR,
            syncWord=LORA_SYNC_WORD,
            power=LORA_POWER_DBM,
            currentLimit=60.0,
            preambleLength=8,
            implicit=False,
            implicitLen=0xFF,
            crcOn=True,
            txIq=False,
            rxIq=False,
            tcxoVoltage=1.6,
            useRegulatorLDO=False,
            blocking=False  # non-blocking mode
        )
        self.lora.setBlockingCallback(False, self._lora_irq_handler)

    @staticmethod
    def _print_line(s: str):
        # Single place for printing back to USB (line-oriented)
        sys.stdout.write(s + "\n")
        sys.stdout.flush()


    def _emit_tx_done(self):
        # Called after TX_DONE interrupt has fired
        toa_ms = 0
        try:
            toa_ms = int(self.lora.getTimeOnAir(self.last_tx["len"]))  # library-provided estimate
        except Exception:
            pass
        elapsed = 0
        try:
            elapsed = utime.ticks_diff(utime.ticks_ms(), self.last_tx["t0"])
        except Exception:
            pass
        info = {
            "bytes": self.last_tx["len"],
            "toa_ms": toa_ms,
            "elapsed_ms": elapsed,
            "status": self.last_tx["status"],
        }
        self._print_line(f"{self._txi_open}{ujson.dumps(info)}{self._txi_close}")

    def _kick_tx_queue(self):
        if self.tx_busy or not self.tx_queue:
            return
        payload = self.tx_queue.pop(0)

        # Record start time and length for a TX-done report
        self.last_tx["len"] = len(payload)
        self.last_tx["t0"] = utime.ticks_ms()

        try:
            ret = self.lora.send(payload)  # non-blocking (we enabled callbacks below)
            # Driver returns (payload_len, status)
            if isinstance(ret, tuple) and len(ret) >= 2:
                self.last_tx["status"] = ret[1]
            else:
                self.last_tx["status"] = ret
            self.tx_busy = True
        except Exception as e:
            self.last_tx["status"] = f"error:{e}"
            self.tx_busy = False

            # still emit a line so the host isn't left hanging
            self._emit_tx_done()

    def _lora_irq_handler(self, events):
        # Called by the driver in non-blocking mode
        try:
            # RX complete?
            if events & SX1262.RX_DONE:
                data, _status = self.lora.recv()  # returns (payload_bytes, status)
                try:
                    text = data.decode("utf-8")
                except Exception:
                    text = data.decode("utf-8", "replace")
                self._print_line(f"{self._open_tag}{text}{self._close_tag}")


            if events & SX1262.TX_DONE:
                # TX complete!
                self.tx_busy = False
                self._emit_tx_done()
                self._kick_tx_queue()
        except Exception:
            # Swallow IRQ exceptions; keep system running
            pass

    def _monitor_usb_connection(self):
        """Non-blocking read of USB serial, extract framed packages, push to TX queue."""

        if not self.poll.poll(0):
            return
        ch = sys.stdin.read(1)
        if not ch:
            return
        self.serial_buf += ch

        # Extract all complete frames in the buffer (handles back-to-back messages)
        while True:
            si = self.serial_buf.find(self._open_tag)
            if si < 0:
                # Optional: drop buffer if it grows too big with junk
                if len(self.serial_buf) > 4096:
                    self.serial_buf = ""
                return
            ei = self.serial_buf.find(self._close_tag, si + len(self._open_tag))
            if ei < 0:
                # not complete yet
                # Trim any leading junk before OPEN_TAG
                if si > 0:
                    self.serial_buf = self.serial_buf[si:]
                return

            # Extract payload and consume the frame
            payload_text = self.serial_buf[si + len(self._open_tag):ei]
            self.serial_buf = self.serial_buf[ei + len(self._close_tag):]

            # Enqueue for TX (encode to bytes; UTF-8)
            self.tx_queue.append(payload_text.encode("utf-8"))
            self._kick_tx_queue()

    def monitor_usb_connection(self, delay_ms=5):
        # Idle loop; LoRa events arrive via IRQ callback
        print("Starting...")
        while True:
            self._monitor_usb_connection()
            utime.sleep_ms(delay_ms)
