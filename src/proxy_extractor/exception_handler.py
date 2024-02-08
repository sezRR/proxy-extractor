import colorama
from colorama import Fore, Style
import sys

import numpy as np
import pandas as pd


class ExceptionHandler:
    def __init__(self) -> None:
        colorama.init()
        sys.excepthook = self.__handle_exception

    def __prepare_log_message(self, color: str, text: str, just_quotes: bool = False) -> str:
        if just_quotes:
            sentence = []
            words = text.split("'")

            for word in words:
                if word == words[1]:
                    sentence.append(f"{color}{word}{Style.RESET_ALL}")
                    continue
                sentence.append(word)

            return ''.join(sentence)

        return f"{color}{text}{Style.RESET_ALL}"

    def __handleFileNotFoundError(self, exc_value):
        file_name = exc_value.filename
        if file_name is None:
            file_name = str(exc_value).split()[0]

        self.danger(
            f"File named '{file_name}' is not found.", True)

    def danger(self, text: str, just_quotes: bool = False):
        print(self.__prepare_log_message(Fore.LIGHTRED_EX, text, just_quotes))

    def info(self, text: str, just_quotes: bool = False):
        print(self.__prepare_log_message(Fore.LIGHTBLUE_EX, text, just_quotes))

    def warning(self, text: str, just_quotes: bool = False):
        print(self.__prepare_log_message(
            Fore.LIGHTYELLOW_EX, text, just_quotes))

    def __handle_exception(self, exc_type, exc_value, exc_traceback):
        self.__handleFileNotFoundError(exc_value)
