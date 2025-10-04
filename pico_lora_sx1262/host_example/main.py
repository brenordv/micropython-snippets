"""
Production-ready, async-capable host-side LoRa serial client.

Key points:
- Async receive interface (async iterator and callback)
- Thread-safe send from any thread/task
- Pluggable transports (pyserial or POSIX stdlib)
- No demo traffic by default

Usage with asyncio:
    import asyncio

    async def main():
        client = LoRaHostClient(port="COM8")
        await client.open()

        # background task to consume messages
        async def consume():
            async for msg in client.messages():
                print("RX:", msg)

        consumer = asyncio.create_task(consume())

        # send when needed
        await client.send_text("hello")

        # run ...
        await asyncio.sleep(60)

        await client.close()
        consumer.cancel()

    asyncio.run(main())
"""

from __future__ import annotations
import sys, time, json, re, platform, socket, threading
from asyncio import Queue, AbstractEventLoop
from typing import Optional, AsyncIterator, Union, Callable
import asyncio


# Protocol tags
OPEN = "<LoRa-Message-Package>"
CLOSE = "</LoRa-Message-Package>"
TXO  = "<Lora-System-Info-Tx-Done>"
TXC  = "</Lora-System-Info-Tx-Done>"

_rx_re = re.compile(rf"{re.escape(OPEN)}(.*?){re.escape(CLOSE)}")
_tx_re = re.compile(rf"{re.escape(TXO)}(.*?){re.escape(TXC)}")


class LoRaHostClient:
    """
    Async-capable LoRa serial client.

    Open/close:
      await open()
      await close()

    Receiving:
      - Consume async iterator: async for payload in client.messages(): ...
      - Or set on_lora_rx callback (optional)

    Sending:
      - await send_text("...")

    Also publishes TX-done events via on_tx_done callback.
    """

    def __init__(self, port: Optional[str] = None, baud_rate: int = 115200):
        self._port: Union[str, None] = port
        self._baud_rate: int = baud_rate

        # Transport adapters (filled in open())
        self._reader: Union[Callable[[int], bytes], None] = None
        self._writer: Union[Callable[[bytes], None], None] = None
        self._closer: Union[Callable[[], None], None] = None
        self._transport: str = "?"  # Either pyserial or posix

        # Run loop thread and coordination
        self._thread: Optional[threading.Thread] = None
        self._stop: threading.Event = threading.Event()

        # Line assembly buffer (bytes)
        self._buf: bytearray = bytearray()

        # Cross-thread queue to deliver parsed events into asyncio loop
        self._queue: Union[Queue[str], None] = None
        self._loop: Union[AbstractEventLoop, None] = None

        # Callbacks (optional)
        self.on_lora_rx: Union[Callable[[str], None], None] = None
        self.on_tx_done: Union[Callable[[str], None], None] = None
        self.on_log: Union[Callable[[str], None], None] = None

        # Sending guard
        self._send_lock: threading.Lock = threading.Lock()

        # Misc
        self._hostname: str = socket.gethostname()

    async def open(self):
        """Open the serial transport and start reader thread."""
        if self._thread and self._thread.is_alive():
            return

        self._open_transport()
        self._log(f"[info] opened {self._transport}:{self._port}")

        # Create per-client queue bound to current loop
        self._loop = asyncio.get_running_loop()  # type: ignore[attr-defined]
        self._queue = asyncio.Queue()            # type: ignore[attr-defined]

        # Start reader thread
        self._stop.clear()
        self._thread = threading.Thread(target=self._reader_loop, name="LoRaHostClientReader", daemon=True)
        self._thread.start()

    async def close(self):
        """Stop reader thread and close transport."""
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        try:
            if self._closer:
                self._closer()
        finally:
            self._reader = self._writer = self._closer = None
            self._thread = None
            self._buf = bytearray()
        self._log("[info] closed")

    async def send_text(self, text: str):
        """Send one framed UTF-8 message."""
        if self._writer is None:
            raise RuntimeError("Client not open")

        frame = f"{OPEN}{text}{CLOSE}\n".encode("utf-8")

        # thread-safe: the writer may block, keep outside event loop via threadpool if needed
        def _write():
            if self._writer is None:
                # Double-checking this here so the IDE will not complain about it being possibly none.
                return

            with self._send_lock:
                self._writer(frame)

        await self._run_in_executor(_write)

    async def messages(self) -> AsyncIterator[str]:
        """Async iterator yielding incoming LoRa payload strings."""
        if not self._queue:
            raise RuntimeError("Client not open")

        while True:
            payload = await self._queue.get()
            yield payload

    def _reader_loop(self):
        try:
            while not self._stop.is_set():
                chunk = self._reader(1024) if self._reader else b""
                if not chunk:
                    time.sleep(0.01)
                    continue

                self._buf.extend(chunk)
                while True:
                    i = self._buf.find(b"\n")
                    if i < 0:
                        break
                    line = self._buf[:i]
                    del self._buf[: i + 1]
                    self._handle_line(line.decode("utf-8", "replace"))

        except Exception as e:
            self._log(f"[error] reader loop: {e}")

    def _handle_line(self, s: str):
        # LoRa RX payloads
        m = _rx_re.search(s)
        if m:
            payload = m.group(1)
            # push to asyncio consumer if present
            if self._queue and self._loop:
                def _put():
                    self._queue.put_nowait(payload)  # type: ignore[attr-defined]
                self._call_soon_threadsafe(_put)
            # invoke callback
            if self.on_lora_rx:
                try:
                    self.on_lora_rx(payload)
                except Exception:
                    pass

        # TX done info
        m = _tx_re.search(s)
        if m:
            raw = m.group(1)
            try:
                info = json.loads(raw)
            except Exception:
                info = {"raw": raw, "error": "json_decode_failed"}
            if self.on_tx_done:
                try:
                    self.on_tx_done(info)
                except Exception:
                    pass

    def _open_transport(self):
        try:
            import serial  # type: ignore
            from serial.tools import list_ports  # type: ignore

            port = self._port
            if port is None:
                candidates = [p.device for p in list_ports.comports()]
                if not candidates:
                    raise RuntimeError("No serial ports found.")
                port = self._pick_port(candidates)

            ser = serial.Serial(port=port, baudrate=self._baud_rate, timeout=0, write_timeout=1)

            def write_bytes(b: bytes) -> None:
                ser.write(b)

            def read_bytes(n: int) -> bytes:
                return ser.read(n)

            def closer():
                try:
                    ser.close()
                except Exception:
                    pass

            self._reader, self._writer, self._closer = read_bytes, write_bytes, closer
            self._port = port
            self._transport = "pyserial"

        except Exception as e:
            if "serial" in str(e).lower() or isinstance(e, ModuleNotFoundError):
                if platform.system() in ("Linux", "Darwin") and self._port:
                    self._open_posix(self._port, self._baud_rate)
                    self._transport = "posix"
                else:
                    raise RuntimeError("PySerial not available and no POSIX path provided.")
            else:
                raise

    def _open_posix(self, path: str, baudrate: int):
        import os, termios, tty, select
        fd = os.open(path, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)

        attrs = termios.tcgetattr(fd)
        tty.setraw(fd)

        # Map common baud rates to termios constants; default to B115200 if unsupported
        baud_map = {
            0: termios.B0, 50: termios.B50, 75: termios.B75, 110: termios.B110,
            134: termios.B134, 150: termios.B150, 200: termios.B200, 300: termios.B300,
            600: termios.B600, 1200: termios.B1200, 1800: termios.B1800, 2400: termios.B2400,
            4800: termios.B4800, 9600: termios.B9600, 19200: termios.B19200, 38400: termios.B38400,
            57600: termios.B57600, 115200: termios.B115200, 230400: termios.B230400,
        }
        bconst = baud_map.get(int(baudrate), termios.B115200)
        termios.cfsetispeed(attrs, bconst)
        termios.cfsetospeed(attrs, bconst)

        attrs[2] = attrs[2] | termios.CLOCAL | termios.CREAD
        attrs[2] = (attrs[2] & ~termios.PARENB)
        attrs[2] = (attrs[2] & ~termios.CSTOPB)
        attrs[2] = (attrs[2] & ~termios.CSIZE) | termios.CS8
        termios.tcsetattr(fd, termios.TCSANOW, attrs)

        def write_bytes(b: bytes) -> None:
            os.write(fd, b)

        def read_bytes(n: int) -> bytes:
            r, _, _ = select.select([fd], [], [], 0)
            if r:
                try:
                    return os.read(fd, n)
                except BlockingIOError:
                    return b""
            return b""

        def closer():
            try:
                os.close(fd)
            except Exception:
                pass

        self._reader = read_bytes
        self._writer = write_bytes
        self._closer = closer

    @staticmethod
    def _pick_port(candidates):
        for d in candidates:
            u = d.upper()
            if "TTYACM" in u or "USBMODEM" in u or u.startswith("COM"):
                return d
        return candidates[0]

    @staticmethod
    async def _run_in_executor(fn):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, fn)

    def _call_soon_threadsafe(self, fn):
        if self._loop:
            try:
                self._loop.call_soon_threadsafe(fn)
            except Exception:
                pass

    def _log(self, s: str):
        if self.on_log:
            try:
                self.on_log(s)
                return
            except Exception:
                pass
        print(s)


# Complete async demo: concurrently receive and periodically send
if __name__ == "__main__":
    if asyncio is None:
        print("This module requires asyncio for CLI usage.")
        sys.exit(1)

    async def _demo():
        port = sys.argv[1] if len(sys.argv) > 1 else None
        client = LoRaHostClient(port=port)
        await client.open()

        async def consume():
            async for m in client.messages():
                print("RX:", m)

        async def produce(interval_s=0.1):
            counter = 0
            host = socket.gethostname()
            while True:
                counter += 1
                msg = f"[{counter}] Hello from {host}"
                await client.send_text(msg)
                print("TX:", msg)
                await asyncio.sleep(interval_s)

        consumer_task = asyncio.create_task(consume())
        producer_task = asyncio.create_task(produce())

        try:
            await asyncio.gather(consumer_task, producer_task)
        except asyncio.CancelledError:
            pass
        finally:
            consumer_task.cancel()
            producer_task.cancel()
            await client.close()

    asyncio.run(_demo())