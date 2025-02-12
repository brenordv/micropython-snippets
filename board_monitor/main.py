import utime

from lib.board_monitor import BoardMonitor

if __name__ == "__main__":
    monitor = BoardMonitor()

    for i in range(10):
        utime.sleep(1)
        status = monitor.get_status()

        print("Board Status:")
        for key, value in status.items():
            print(f"{key}: {value}")
