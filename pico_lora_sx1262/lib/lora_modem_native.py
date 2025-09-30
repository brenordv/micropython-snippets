import sys, uselect, utime, ujson
from machine import Pin, SPI
from lib.lora import SX1262

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

# Native driver IRQ constants (from the source code you provided)
_IRQ_TX_DONE = const(1 << 0)  # = 0x01
_IRQ_RX_DONE = const(1 << 1)  # = 0x02


class LoRaModemNative:
    """LoRa Modem using native MicroPython sx126x driver with identical interface to original"""
    
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
        
        # IRQ pending flag for main loop processing
        self._irq_pending = False

        # Initialize SPI for official driver
        self.spi = SPI(
            SPI_ID,
            baudrate=2_000_000,  # Official driver uses 2MHz by default
            polarity=0, phase=0,
            sck=Pin(PIN_SCK), mosi=Pin(PIN_MOSI), miso=Pin(PIN_MISO)
        )

        # Configure LoRa parameters for official driver
        lora_config = {
            "freq_khz": int((LORA_FREQ_MHZ_US if use_us_freq else LORA_FREQ_MHZ_EU) * 1000),
            "sf": LORA_SF,
            "bw": str(int(LORA_BW_KHZ)),  # Must be string like "125"
            "coding_rate": LORA_CR,
            "syncword": LORA_SYNC_WORD,
            "output_power": LORA_POWER_DBM,
            "preamble_len": 8,
            "invert_iq_rx": False,
            "invert_iq_tx": False
        }

        # Initialize the official SX1262 driver with proper parameters
        self.lora = SX1262(
            spi=self.spi,
            cs=Pin(PIN_CS),
            busy=Pin(PIN_BUSY),
            dio1=Pin(PIN_IRQ),
            dio2_rf_sw=True,  # Use DIO2 as RF switch for Waveshare HAT
            dio3_tcxo_millivolts=1600,  # 1.6V TCXO
            dio3_tcxo_start_time_us=1000,
            reset=Pin(PIN_RST),
            lora_cfg=lora_config,  # Pass configuration during initialization
            ant_sw=None
        )
        
        # Set up IRQ callback for non-blocking operation
        self.lora.set_irq_callback(self._on_irq)
        
        # Start in continuous receive mode
        self._start_receiving()

    @staticmethod
    def _print_line(s: str):
        # Single place for printing back to USB (line-oriented)
        sys.stdout.write(s + "\n")
        sys.stdout.flush()

    def _emit_tx_done(self):
        # Called after TX_DONE interrupt has fired
        toa_ms = 0
        try:
            toa_ms = int(self.lora.get_time_on_air_us(self.last_tx["len"]) / 1000)  # Convert us to ms
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

    def _start_receiving(self):
        """Start the modem in continuous receive mode"""
        try:
            # Start continuous receive using official API
            self.lora.start_recv(timeout_ms=None, continuous=True)
        except Exception as e:
            print(f"Error starting receive: {e}")

    def _on_irq(self):
        """IRQ callback from official driver - schedule check in main loop"""
        # Note: This runs in IRQ context, so just set a flag
        # The actual processing happens in _check_lora_events()
        self._irq_pending = True

    def _kick_tx_queue(self):
        if self.tx_busy or not self.tx_queue:
            return
        payload = self.tx_queue.pop(0)

        # Record start time and length for a TX-done report
        self.last_tx["len"] = len(payload)
        self.last_tx["t0"] = utime.ticks_ms()

        try:
            # Use official driver's synchronous send method in non-blocking fashion
            # First prepare the send
            self.lora.prepare_send(payload)
            # Then start it (returns a pin object for IRQ if available)
            self.lora.start_send()
            self.last_tx["status"] = "sending"
            self.tx_busy = True
        except Exception as e:
            self.last_tx["status"] = f"error:{e}"
            self.tx_busy = False
            # still emit a line so the host isn't left hanging
            self._emit_tx_done()

    def _check_lora_events(self):
        """Check for LoRa TX/RX events using official driver polling - called frequently"""
        try:
            # Process any pending IRQ events
            if self._irq_pending:
                self._irq_pending = False
                
                # Check for completed send using official API
                if self.tx_busy:
                    send_result = self.lora.poll_send()
                    if send_result is not True:  # True means still sending
                        # Send completed (either success or error)
                        self.tx_busy = False
                        if send_result is False:
                            self.last_tx["status"] = "completed"
                        else:
                            self.last_tx["status"] = f"error:{send_result}"
                        self._emit_tx_done()
                        self._kick_tx_queue()
                        # Restart receiving after TX
                        self._start_receiving()
                
                # Check for received packets using official API
                rx_packet = self.lora.poll_recv()
                if rx_packet is not True and rx_packet is not False and rx_packet is not None:
                    # We have a received packet (RxPacket object)
                    try:
                        text = bytes(rx_packet).decode("utf-8")
                    except Exception:
                        text = bytes(rx_packet).decode("utf-8", "replace")
                    self._print_line(f"{self._open_tag}{text}{self._close_tag}")
            
            # Also do periodic polling for robustness (in case IRQ is missed)
            else:
                # Quick poll without full processing
                if self.tx_busy:
                    send_result = self.lora.poll_send()
                    if send_result is not True:
                        self._irq_pending = True  # Trigger full processing next time
                
                rx_packet = self.lora.poll_recv()
                if rx_packet is not True and rx_packet is not False and rx_packet is not None:
                    self._irq_pending = True  # Trigger full processing next time
                
        except Exception as e:
            # Swallow exceptions; keep system running
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
        # Idle loop; LoRa events are handled via polling (native driver requirement)
        print("Starting Native LoRa Modem...")
        while True:
            self._monitor_usb_connection()
            # Native driver requires frequent polling for TX/RX events
            self._check_lora_events()
            utime.sleep_ms(delay_ms)