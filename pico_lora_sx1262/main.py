from lib.lora_modem import LoRaModem


def main():
    modem = LoRaModem()
    modem.monitor_usb_connection()


if __name__ == '__main__':
    main()
