from colorama import Fore, Style
from enum import Enum


class MessageType(Enum):
    SUCCESS = 0
    WARNING = 1
    ERROR = 2
    INFO = 3


def show_message(msg, msg_type=MessageType.INFO):
    color = None
    start_str = ''
    if msg_type == MessageType.SUCCESS:
        color = Fore.GREEN
        start_str = '[✔]'
    elif msg_type == MessageType.WARNING:
        color = Fore.YELLOW
        start_str = '[⚠]'
    elif msg_type == MessageType.ERROR:
        color = Fore.RED
        start_str = '[✘]'
    else:
        color = Fore.BLUE
        start_str = '[ℹ]'
    print(color + f"{start_str} " + Fore.RESET + msg)
