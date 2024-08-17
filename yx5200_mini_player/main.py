import utime

from lib.audio_player import AudioPlayer


print("Initializing YX5200 Mini MP3 Player...")
#player = AudioPlayer(uart=2, tx_pin=17, rx_pin=16, busy_pin=22)
player = AudioPlayer(uart=0, tx_pin=0, rx_pin=1, busy_pin=22)

# Set volume (0-30)
player.set_volume(30)

# Try to play the specific file
player.play(1) # This should play 001.mp3 - first file on the SD card

# Wait and check if it's playing
for _ in range(10):
    utime.sleep(1)
    is_playing = player.is_playing()
    print(f"Is playing: {is_playing}")

print("Done!")
