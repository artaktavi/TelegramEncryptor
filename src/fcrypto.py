import sys
from pathlib import Path

from cryptographers import caesar_cryptographer
from cryptographers import vigener_cryptographer
from cryptographers import vernam_cryptographer

caesar_crypto = caesar_cryptographer.CaesarCryptographer()
vigener_crypto = vigener_cryptographer.VigenerCryptographer()
vernam_crypto = vernam_cryptographer.VernamCryptographer()

class CommandHelper:
    def __init__(self):
        self.mode_text = "Mode: "
        self.cypher_text = "Cypher: "
        self.input_file_text = "Input file: "
        self.error_text = "ERROR"

    def check_mode(self, mode : str) -> int:
        if mode == "-e":
            return "encypher"
        elif mode == "-d":
            return "decypher"
        elif mode == "-g":
            return "generate key"
        elif mode == "-h":
            return "hack"
        else:
            return error_text

    def check_cypher(self, cypher : str) -> str:
        if cypher == "vernam":
            return "Vernam"
        elif cypher == "vigener":
            return "Vigener"
        elif cypher == "caesar":
            return "Caesar"
        else:
            return error_text

    def check_input_file(self, input : str) -> str:
        if input != "" and not Path(input).is_file():
            return error_text
        else:
            return input

    def execute_encypher(self, cypher: str, input: str, output: str, key: str) -> str:
        if cypher == "vernam":
            return vernam_crypto.encypher(input, output, key)
        elif cypher == "vigener":
            return vigener_crypto.encypher(input, output, key)
        else:
            return caesar_crypto.encypher(input, output, key)
  
    def execute_decypher(self, cypher: str, input: str, output: str, key: str) -> str:
        if cypher == "vernam":
            return vernam_crypto.decypher(input, output, key)
        elif cypher == "vigener":
            return vigener_crypto.decypher(input, output, key)
        else:
            return caesar_crypto.decypher(input, output, key)

    def execute_generate(self, cypher: str) -> str:
        if cypher == "vernam":
            return vernam_crypto.generate_key()
        elif cypher == "vigener":
            return vigener_crypto.generate_key()
        else:
            return caesar_crypto.generate_key()

    def execute_hack(self, cypher: str, input: str) -> str:
        if cypher == "vernam":
            return vernam_crypto.hack(input)
        elif cypher == "vigener":
            return vigener_crypto.hack(input)
        else:
            return caesar_crypto.hack(input)

    def process_request(self, args: list) -> str:
        ans = ""
        mode_check_res = self.check_mode(args[0])
        ans += self.mode_text + mode_check_res + '\n'
        if mode_check_res == self.error_text:
            ans += ": incorrect mode"
            return ans
        cypher_check_res = self.check_cypher(args[1])
        ans += self.cypher_text + cypher_check_res + '\n'
        if cypher_check_res == self.error_text:
            ans += ": incorrect cypher"
            return ans
        if len(args) > 2:
            input_file_check_res = self.check_input_file(args[2])
            ans += self.input_file_text + input_file_check_res + '\n'
            if input_file_check_res == self.error_text:
                ans += ": incorrect input file"
                return ans
        if mode_check_res == "encypher":
            ans += self.execute_encypher(args[1], args[2], args[3], args[4])
        elif mode_check_res == "decypher":
            ans += self.execute_decypher(args[1], args[2], args[3], args[4])
        elif mode_check_res == "generate key":
            ans += self.execute_generate(args[1])
        else:
            ans += self.execute_hack(args[1], args[2])
        return ans
