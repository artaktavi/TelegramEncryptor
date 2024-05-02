import random
from collections import Counter
from .cryptographer import Cryptographer


class CaesarCryptographer(Cryptographer):
    def encypher(self, input_path: str, output_path: str, key: str) -> str:
        """Encypher file on input_path using a key to output_path
        (creates of overwrites it if exists)."""
        with open(input_path, "r") as input_file:
            with open(output_path, "w") as output_file:
                for symbol in input_file.read():
                    output_file.write(chr(ord(symbol) + int(key)))
        return (input_path + " file was successfully encyphered to: " + output_path)

    def decypher(self, input_path: str, output_path: str, key: str) -> str:
        """Decypher file on input_path using a key to output_path
        (creates of overwrites it if exists)."""
        with open(input_path, "r") as input_file:
            with open(output_path, "w") as output_file:
                for symbol in input_file.read():
                    output_file.write(chr(ord(symbol) - int(key)))
        return (input_path + " file was successfully decyphered to: " + output_path)

    def generate_key(self) -> str:
        """Generates key for the same cypher type."""
        return str(random.randint(3, 50))

    def hack(self, input_path: str) -> str:
        """Hack file on input_path and returns cipher code
        (decypher without key)."""
        with open(input_path, "r") as input_file:
            input_text = input_file.read()
            most_frequent = Counter(input_text).most_common(1)[0]
            decode_key = ord(most_frequent[0]) - ord(" ")
        return str(decode_key)

