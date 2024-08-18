# YX5200 DF Player Mini
A very crude implementation of the YX5200 DF Player Mini. 
This is a simple implementation that allows you to play audio files from a microSD card.

Right now you can only play a file and use the busy pin to check if file is playing.

To use this, copy the `lib` folder to your project.

## Hardware
- YX5200 DF Player Mini
- Raspberry Pi Pico

### Raspberry Pi Pico Pinout
I made it work with the Pico using the following pins:
- YX5200 VCC -> Pico VSYS
- YX5200 GND -> Pico GND (any)
- YX5200 RX -> Pico TX UART 0 (GPIO 16)
- YX5200 TX -> Pico RX UART 0 (GPIO 17)
- YX5200 BUSY -> Pico GPIO 22
- YX5200 SPK1 -> Speaker Positive
- YX5200 SPK2 -> Speaker Negative

![Raspberry_Pi_Pico_Pinout.png](.assets%2FRaspberry_Pi_Pico_Pinout.png)

### DF Player Pinout
![YX5200_MP3player.png](.assets%2FYX5200_MP3player.png)
![YX5200_MP3player_pinouts.png](.assets%2FYX5200_MP3player_pinouts.png)

### DF Player Datasheet
[DFPlayer Mini Manual.pdf](.assets%2FDFPlayer%20Mini%20Manual.pdf)

## AudioPlayer Class
### Methods

#### `__init__(self, uart, tx_pin, rx_pin, busy_pin, baud_rate=9600)`
Initializes the `AudioPlayer` with the specified UART interface, TX and RX pins, busy pin, and baud rate.

- **Parameters:**
  - `uart` (int): The UART interface number.
  - `tx_pin` (int): The pin number for the UART TX.
  - `rx_pin` (int): The pin number for the UART RX.
  - `busy_pin` (int): The pin number for the busy signal.
  - `baud_rate` (int, optional): The baud rate for UART communication. Default is 9600.

#### `play(self, track_number)`
Plays the specified track number.

- **Parameters:**
  - `track_number` (int): The track number to play.

#### `set_volume(self, volume)`
Sets the volume level.

- **Parameters:**
  - `volume` (int): The volume level (0-30).

#### `is_playing(self)`
Checks if a track is currently playing.

- **Returns:**
  - `bool`: `True` if a track is playing, otherwise `False`.


# Attributions
Specs images from this repo: https://github.com/Mark-MDO47/AudioPlayer-YX5200
