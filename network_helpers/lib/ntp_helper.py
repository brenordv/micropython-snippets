import ntptime
import time


class NtpHelper:
    def __init__(self, host=None, resync_period=3600):
        if host:
            ntptime.host = host

        self.resync_period = resync_period
        self.last_sync = None
        self.sync()

    def sync(self):
        ntptime.settime()
        self.last_sync = time.time()

    def get_local_time(self):
        if not self.last_sync or (time.time() - self.last_sync) > self.resync_period:
            self.sync()

        local_time = time.localtime()

        ms = time.ticks_ms()

        return f"{local_time[0]}-{local_time[1]:02d}-{local_time[2]:02d}T{local_time[3]:02d}:{local_time[4]:02d}:{local_time[5]:02d}.{ms}Z"
