import random
from .cryptographer import Cryptographer


class VernamCryptographer(Cryptographer):
    def cypher(self, input_path: str, output_path: str, key: str) -> None:
        """Internal function that cypher input_path file to output_path file"""
        with open(input_path, "r") as input_file:
            with open(output_path, "w") as output_file:
                index = 0
                mod = len(key)
                for symbol in input_file.read():
                    output_file.write(chr(ord(symbol) ^ ord(key[index])))
                    index += 1
                    index %= mod

    def encypher(self, input_path: str, output_path: str, key: str) -> str:
        """Encypher file on input_path using a key to output_path
        (creates of overwrites it if exists)."""
        self.cypher(input_path, output_path, key)
        return (input_path + " file was successfully encyphered to: " + output_path)

    def decypher(self, input_path: str, output_path: str, key: str) -> str:
        """Decypher file on input_path using a key to output_path
        (creates of overwrites it if exists)."""
        self.cypher(input_path, output_path, key)
        return (input_path + " file was successfully decyphered to: " + output_path)

    def generate_key(self) -> str:
        """Generates key for the same cypher type."""
        return str(
            "".join(
                chr(ord("A") + random.randint(-16, 25))
                for x in range(random.randint(10, 30))
            )
        )

    def hack(self, input_path: str) -> str:
        """Hack file on input_path and returns cipher code
        (decypher without key)."""
        return "No possibility for hacking vernam cipher"

