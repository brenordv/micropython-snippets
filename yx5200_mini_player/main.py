import utime

from lib.audio_player import AudioPlayer


print("Initializing YX5200 Mini MP3 Player...")
player = AudioPlayer(uart=0, tx_pin=16, rx_pin=17, busy_pin=22)

# Set volume (0-30)
player.set_volume(10)

# Try to play the specific file
player.play_sync(1) # This should play 001.mp3 - first file on the SD card

print("Done!")
