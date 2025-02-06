import time

from lib.onboard_led import OnboardLED


class MorseLED(OnboardLED):
    """
    A class to control the onboard LED and send Morse code messages.
    Inherits from OnboardLED.
    """

    # Morse code dictionary (letters, digits, and common punctuation)
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '0': '-----', '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
        '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
        ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
        '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
    }

    DOT_DURATION = 0.2  # Duration of a dot in seconds
    DASH_DURATION = DOT_DURATION * 3
    SYMBOL_PAUSE = DOT_DURATION  # Pause between symbols in a character
    CHARACTER_PAUSE = DOT_DURATION * 3  # Pause between characters
    WORD_PAUSE = DOT_DURATION * 7  # Pause between words

    def __init__(self, pin_identifier="LED"):
        """Initialize the MorseLED class."""
        super().__init__(pin_identifier)

    def morse_code(self, text: str, times: int):
        """
        Blink the LED to send a Morse code message.

        Args:
            text (str): The message to be sent in Morse code.
            times (int): Number of times to repeat the message. If -1, repeat forever.
        """
        # Convert the text to uppercase to match the Morse dictionary
        text = text.upper()

        def send_symbol(symbol):
            """Send a single Morse code symbol (dot or dash)."""
            if symbol == '.':
                self.on()
                time.sleep(self.DOT_DURATION)
            elif symbol == '-':
                self.on()
                time.sleep(self.DASH_DURATION)
            self.off()
            time.sleep(self.SYMBOL_PAUSE)

        def send_character(character):
            """Send a single character in Morse code."""
            if character in self.MORSE_CODE_DICT:
                code = self.MORSE_CODE_DICT[character]
                for symbol in code:
                    send_symbol(symbol)
                time.sleep(self.CHARACTER_PAUSE)

        def send_message(message):
            """Send the entire message in Morse code."""
            words = message.split(' ')
            for word in words:
                for character in word:
                    send_character(character)
                time.sleep(self.WORD_PAUSE)

        # Repeat the message the specified number of times
        while times != 0:
            send_message(text)
            times -= 1 if times > 0 else 0
