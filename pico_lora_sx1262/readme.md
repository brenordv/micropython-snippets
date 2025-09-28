> STILL TESTING.

# Waveshare Pico LoRa SX1262 Controller
This project provides a comprehensive LoRa communication controller for the Raspberry Pi Pico W with 
Waveshare Pico-LoRa-SX1262 HAT. 

It implements a non-blocking LoRa "modem" with framed message protocol over USB serial, supporting both transmission
and reception with callback-based event handling.

Usually I create more of a controller/service/wrapper type of thing, but with this one I decided to use a different 
approach and use the Pi Pico + LoRa Hat as a type of modem for LoRa. This way I can any other application with it.

If you want, you can change the tags that are being used in the code to identify when the message is ready to be received.
Think of the tags as envelopes.

Right now, when the host sends a message to out LoRa modem, it waits for the closing tag before sending the message.

## Installation
Just copy the `lib` folder to your board.
Initialize LoRa Modem class and you're good to go.

## Hardware
- Raspberry Pi Pico or Pico W
- Waveshare Pico-LoRa-SX1262 HAT

### Raspberry Pi Pico Pinout
![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### Waveshare Pico-LoRa-SX1262 HAT Pinout
![Pico-LoRa-SX1262-868M-details-inter.jpg](.assets%2FPico-LoRa-SX1262-868M-details-inter.jpg)

The HAT connects to the Pico via SPI1 with the following pin mapping:
- **SPI1**: SCK=GP10, MOSI=GP11, MISO=GP12
- **CS/NSS**: GP3
- **DIO1/IRQ**: GP20
- **RST**: GP15
- **BUSY**: GP2

### Waveshare Pico-LoRa-SX1262 HAT Datasheet
[DS_SX1261-2_V1.2](.assets%2FDS_SX1261-2_V1.2)

## Configuration
The main script supports configurable LoRa parameters:
- **Frequency**: 915.0 MHz (US915) / 868.0 MHz (EU868)
- **Bandwidth**: 125.0 kHz
- **Spreading Factor**: 7 (range: 5-12)
- **Coding Rate**: 8 (denominator: 5-8)
- **Output Power**: 14 dBm
- **Sync Word**: 0x12 (private networks)

## Host Protocol
The system uses a framed message protocol over USB serial:

### Send Message (Host → LoRa)
```
<LoRa-Message-Package>your text here</LoRa-Message-Package>
```

### Receive Message (LoRa → Host)
```
<LoRa-Message-Package>peer text here</LoRa-Message-Package>
```

### TX Completion Notification
```
<Lora-System-Info-Tx-Done>{"bytes":N,"toa_ms":X,"elapsed_ms":Y,"status":Z}</Lora-System-Info-Tx-Done>
```

## Host Example
The `host_example` directory contains a Python utility for communicating with the LoRa controller. 
It supports both PySerial and native POSIX serial communication.

### Prerequisites
- Python 3.13 or higher
- PySerial library (optional, POSIX fallback available)

### Usage
```bash
cd host_example
python main.py
```

## SX1262 Class
### Methods

#### `__init__(self, spi_bus, clk, mosi, miso, cs, irq, rst, gpio)`
Initializes the SX1262 LoRa transceiver.

- **Parameters:**
  - `spi_bus` (int): SPI bus number
  - `clk` (int): SPI clock pin
  - `mosi` (int): SPI MOSI pin
  - `miso` (int): SPI MISO pin
  - `cs` (int): Chip select pin
  - `irq` (int): Interrupt pin (DIO1)
  - `rst` (int): Reset pin
  - `gpio` (int): BUSY pin

#### `begin(self, freq=434.0, bw=125.0, sf=9, cr=7, syncWord=SX126X_SYNC_WORD_PRIVATE, power=14, currentLimit=60.0, preambleLength=8, implicit=False, implicitLen=0xFF, crcOn=True, txIq=False, rxIq=False, tcxoVoltage=1.6, useRegulatorLDO=False, blocking=True)`
Configures and initializes the LoRa radio.

- **Parameters:**
  - `freq` (float): Operating frequency in MHz
  - `bw` (float): Bandwidth in kHz
  - `sf` (int): Spreading factor (5-12)
  - `cr` (int): Coding rate (5-8)
  - `syncWord` (int): Synchronization word
  - `power` (int): Output power in dBm
  - `currentLimit` (float): Current limit in mA
  - `preambleLength` (int): Preamble length
  - `implicit` (bool): Use implicit header mode
  - `implicitLen` (int): Implicit packet length
  - `crcOn` (bool): Enable CRC
  - `txIq` (bool): Invert TX IQ
  - `rxIq` (bool): Invert RX IQ
  - `tcxoVoltage` (float): TCXO voltage
  - `useRegulatorLDO` (bool): Use LDO regulator
  - `blocking` (bool): Use blocking mode

- **Returns:**
  - `int`: Error code (ERR_NONE on success)

#### `send(self, data)`
Sends data over LoRa (blocking or non-blocking based on configuration).

- **Parameters:**
  - `data` (bytes/bytearray): Data to transmit

- **Returns:**
  - `tuple`: (payload_length, status) in non-blocking mode
  - `int`: Status code in blocking mode

#### `recv(self, len=0, timeout_en=False, timeout_ms=0)`
Receives data from LoRa (blocking or non-blocking based on configuration).

- **Parameters:**
  - `len` (int): Expected length (0 for any length)
  - `timeout_en` (bool): Enable timeout (blocking mode only)
  - `timeout_ms` (int): Timeout in milliseconds (blocking mode only)

- **Returns:**
  - `tuple`: (received_data, status)

#### `setFrequency(self, freq, calibrate=True)`
Sets the operating frequency.

- **Parameters:**
  - `freq` (float): Frequency in MHz (150-960 MHz)
  - `calibrate` (bool): Perform image calibration

- **Returns:**
  - `int`: Error code

#### `setOutputPower(self, power)`
Sets the transmission power.

- **Parameters:**
  - `power` (int): Output power in dBm (-9 to 22 dBm)

- **Returns:**
  - `int`: Error code

#### `setBlockingCallback(self, blocking, callback=None)`
Configures blocking/non-blocking mode and interrupt callback.

- **Parameters:**
  - `blocking` (bool): Enable blocking mode
  - `callback` (function): Callback function for interrupt events

- **Returns:**
  - `int`: Error code

#### `getTimeOnAir(self, len_)`
Calculates time-on-air for a packet.

- **Parameters:**
  - `len_` (int): Packet length in bytes

- **Returns:**
  - `int`: Time-on-air in microseconds

#### `getRSSI(self)`
Gets the RSSI of the last received packet.

- **Returns:**
  - `float`: RSSI in dBm

#### `getSNR(self)`
Gets the SNR of the last received packet (LoRa mode only).

- **Returns:**
  - `float`: SNR in dB

## Features
- **Non-blocking Operation**: Interrupt-driven TX/RX with callback support
- **Framed Protocol**: Robust message framing for host communication
- **TX Status Reporting**: Detailed transmission completion information
- **Regional Support**: Configurable for different LoRa regions
- **Host Integration**: Python utility for easy host-side communication
- **Error Handling**: Comprehensive error reporting and recovery

## References
- WaveShare SX1262 driver originally from: https://github.com/ehong-tl/micropySX126X/tree/master/lib
