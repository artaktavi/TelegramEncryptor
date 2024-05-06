import random
from .cryptographer import Cryptographer


class VigenerCryptographer(Cryptographer):
    def __init__(self):
        self.edge_code = ord("A")

    def encypher(self, input_path: str, output_path: str, key: str) -> str:
        """Encypher file on input_path using a key to output_path
        (creates of overwrites it if exists)."""
        with open(input_path, "r") as input_file:
            with open(output_path, "w") as output_file:
                index = 0
                mod = len(key)
                for symbol in input_file.read():
                    output_file.write(
                        chr(ord(symbol) + (ord(key[index]) - self.edge_code))
                    )
                    index += 1
                    index %= mod
        return (input_path + " file was successfully encyphered to: " + output_path)

    def decypher(self, input_path: str, output_path: str, key: str) -> str:
        """Decypher file on input_path using a key to output_path
        (creates of overwrites it if exists)."""
        with open(input_path, "r") as input_file:
            with open(output_path, "w") as output_file:
                index = 0
                mod = len(key)
                for symbol in input_file.read():
                    output_file.write(
                        chr(ord(symbol) - (ord(key[index]) - self.edge_code))
                    )
                    index += 1
                    index %= mod
        return (input_path + " file was successfully decyphered to: " + output_path)

    def generate_key(self) -> str:
        """Generates key for the same cypher type."""
        return str(
            "".join(
                chr(self.edge_code + random.randint(0, 25))
                for x in range(random.randint(10, 30))
            )
        )

    def hack(self, input_path: str) -> str:
        """Hack file on input_path and returns cipher code
        (decypher without key)."""
        return "No possibility for hacking vigener cipher"

