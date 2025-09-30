"""
Host-side utility to talk to a microcontroller over a serial TTY.

It continuously:
- Sends a framed message every 15 seconds with hostname and message counter
- Parses incoming lines for:
  - LoRa payloads framed by <LoRa-Message-Package>...</LoRa-Message-Package>
  - TX completion info framed by <Lora-System-Info-Tx-Done>...</Lora-System-Info-Tx-Done> (JSON)

Runs until interrupted by user (Ctrl+C).
"""

import sys, time, json, re, platform, socket

# If you don't know, you can run: `py -m serial.tools.list_ports -v` to find out.
PORT = "COM8"  # e.g. "COM5" (Windows), "/dev/ttyACM0" (Linux), "/dev/tty.usbmodemXXXX" (macOS)

OPEN = "<LoRa-Message-Package>"
CLOSE = "</LoRa-Message-Package>"
TXO  = "<Lora-System-Info-Tx-Done>"
TXC  = "</Lora-System-Info-Tx-Done>"

rx_tag = re.compile(rf"{re.escape(OPEN)}(.*?){re.escape(CLOSE)}")
tx_tag = re.compile(rf"{re.escape(TXO)}(.*?){re.escape(TXC)}")

def _send_frame(write_bytes, text: str):
    """Write one UTF-8 encoded line framed by OPEN/CLOSE tags via the provided writer."""
    frame = f"{OPEN}{text}{CLOSE}\n".encode("utf-8")
    write_bytes(frame)

def _read_lines(read_bytes, timeout_s=0.1):
    """
    Yield decoded lines (str) from a non-blocking byte reader for up to `timeout_s` seconds.

    The generator polls `read_bytes(chunk_size)` and splits on '\n', decoding with
    UTF-8 and 'replace' error handling. It yields what arrives within the time window.
    """
    buf = bytearray()
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        chunk = read_bytes(1024)
        if chunk:
            buf.extend(chunk)
            while b"\n" in buf:
                line, _, buf = buf.partition(b"\n")
                yield line.decode("utf-8", "replace")
        else:
            time.sleep(0.01)

def _run_with_pyserial(port_hint=None):
    """
    Use pyserial to open a 115200-8N1 port, auto-selecting a likely device if needed,
    continuously send messages every 15s and parse LoRa RX and TX-DONE events.
    """
    import serial
    from serial.tools import list_ports

    port = port_hint
    if port is None:
        # Pick the first reasonable port (Pico shows up as ACM/usbmodem typically)
        candidates = [p.device for p in list_ports.comports()]  # list available ports
        if not candidates:
            raise RuntimeError("No serial ports found.")
        # naive heuristic
        for d in candidates:
            if "ttyACM" in d or "usbmodem" in d or d.upper().startswith("COM"):
                port = d; break
        if port is None:
            port = candidates[0]
        print(f"[info] Using port: {port}")

    ser = serial.Serial(port=port, baudrate=115200, timeout=0, write_timeout=1)
    def write_bytes(b: bytes) -> None:
        """Thin wrapper around Serial.write()."""
        ser.write(b)

    def read_bytes(n: int) -> bytes:
        """Thin wrapper around Serial.read() with non-blocking timeout=0 semantics."""
        return ser.read(n)

    try:
        hostname = socket.gethostname()
        message_count = 0
        last_send_time = 0
        
        print(f"[info] Starting continuous communication. Press Ctrl+C to stop.")
        print(f"[info] Hostname: {hostname}")
        
        while True:
            current_time = time.time()
            
            # Send message every 15 seconds
            if current_time - last_send_time >= 1:
                message_count += 1
                message = f"[{message_count}] Hello world from {hostname}"
                _send_frame(write_bytes, message)
                print(f"[sent] {message}")
                last_send_time = current_time
            
            # Check for incoming messages
            for line in _read_lines(read_bytes, timeout_s=0.25):
                if (m := rx_tag.search(line)):
                    print("LoRa RX:", m.group(1))
                if (m := tx_tag.search(line)):
                    print("TX DONE:", json.loads(m.group(1)))
            
            time.sleep(0.1)  # Small delay to prevent busy-waiting
            
    except KeyboardInterrupt:
        print("\n[info] Stopped by user.")
    finally:
        ser.close()

def _run_with_posix_stdlib(path):
    """
    POSIX fallback without pyserial: open `path` and configure 115200-8N1 using
    termios/select, continuously send messages every 15s and parse events.
    """
    # Pure-stdlib POSIX (Linux/macOS) fallback using termios/select
    import os, termios, tty, fcntl, select
    fd = os.open(path, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)

    try:
        # Configure raw mode, 115200 8N1
        attrs = termios.tcgetattr(fd)
        tty.setraw(fd)
        # set speeds
        termios.cfsetispeed(attrs, termios.B115200)
        termios.cfsetospeed(attrs, termios.B115200)
        # 8N1: 8 data bits, no parity, 1 stop
        attrs[2] = attrs[2] | termios.CLOCAL | termios.CREAD  # c_cflag
        attrs[2] = (attrs[2] & ~termios.PARENB)               # no parity
        attrs[2] = (attrs[2] & ~termios.CSTOPB)               # 1 stop
        attrs[2] = (attrs[2] & ~termios.CSIZE) | termios.CS8  # 8 data
        termios.tcsetattr(fd, termios.TCSANOW, attrs)

        # make non-blocking read with select
        def write_bytes(b: bytes) -> None:
            """Write bytes to the TTY file descriptor."""
            os.write(fd, b)

        def read_bytes(n: int) -> bytes:
            """
            Non-blocking read from the TTY using select() polling.
            Returns empty bytes if no data is available.
            """
            r, _, _ = select.select([fd], [], [], 0)
            if r:
                try:
                    return os.read(fd, n)
                except BlockingIOError:
                    return b""
            return b""

        hostname = socket.gethostname()
        message_count = 0
        last_send_time = 0
        partial = b""
        
        print(f"[info] Starting continuous communication (POSIX). Press Ctrl+C to stop.")
        print(f"[info] Hostname: {hostname}")
        
        while True:
            current_time = time.time()
            
            # Send message every 15 seconds
            if current_time - last_send_time >= 15:
                message_count += 1
                message = f"[{message_count}] Hello world from {hostname}"
                _send_frame(write_bytes, message)
                print(f"[sent] {message}")
                last_send_time = current_time
            
            # Check for incoming messages
            chunk = read_bytes(1024)
            if chunk:
                partial += chunk
                while b"\n" in partial:
                    line, _, partial = partial.partition(b"\n")
                    s = line.decode("utf-8", "replace")
                    if (m := rx_tag.search(s)):
                        print("LoRa RX:", m.group(1))
                    if (m := tx_tag.search(s)):
                        print("TX DONE:", json.loads(m.group(1)))
            else:
                time.sleep(0.1)  # Small delay to prevent busy-waiting

    except KeyboardInterrupt:
        print("\n[info] Stopped by user (POSIX).")
    finally:
        os.close(fd)

if __name__ == "__main__":
    try:
        # We try to guess which runtime to use.
        import serial  # noqa: F401
        _run_with_pyserial(PORT)
    except Exception as e:
        if "serial" in str(e).lower() or isinstance(e, ModuleNotFoundError):
            if platform.system() in ("Linux", "Darwin") and PORT:
                print("[warn] PySerial unavailable. Falling back to POSIX stdlib.")
                _run_with_posix_stdlib(PORT)
            else:
                raise SystemExit(
                    "PySerial is not installed and no POSIX fallback path was provided.\n"
                    "Install pyserial: python -m pip install pyserial"
                )
        else:
            raise
