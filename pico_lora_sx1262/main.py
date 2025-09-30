"""
Main entry point - choose your LoRa driver implementation:

Option 1: 3rd party driver (IRQ-based)
Option 2: Native MicroPython driver (official, polling-based)

Both have identical functionality and interface!
"""

_use_native_driver = True

if _use_native_driver:
    from lib.lora_modem_native import LoRaModemNative as LoRaModem
else:
    from lib.lora_modem import LoRaModem


def main():
    # Works identically with either driver!
    modem = LoRaModem(use_us_freq=True)  # Set to False for EU frequencies
    modem.monitor_usb_connection()


if __name__ == '__main__':
    main()
