class Cryptographer:
    def encypher(self, input_path: str, output_path: str, key: str) -> str:
        """Encypher file on input_path using a key to output_path
        (creates of overwrites it if exists)."""
        pass

    def decypher(self, input_path: str, output_path: str, key: str) -> str:
        """Decypher file on input_path using a key to output_path
        (creates of overwrites it if exists)."""
        pass

    def generate_key(self) -> str:
        """Generates key for the same cypher type."""
        pass

    def hack(self, input_path: str) -> str:
        """Hack file on input_path and returns cipher code
        (decypher without key)."""
        pass

