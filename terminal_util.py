import os


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVERTED = '\033[7m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[30;1m'
    BRIGHT_RED = '\033[31;1m'
    BRIGHT_GREEN = '\033[32;1m'
    BRIGHT_YELLOW = '\033[33;1m'
    BRIGHT_BLUE = '\033[34;1m'
    BRIGHT_MAGENTA = '\033[35;1m'
    BRIGHT_CYAN = '\033[36;1m'
    BRIGHT_WHITE = '\033[37;1m'
    BACKGROUND_BLACK = '\033[40m'
    BACKGROUND_RED = '\033[41m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_YELLOW = '\033[43m'
    BACKGROUND_BLUE = '\033[44m'
    BACKGROUND_MAGENTA = '\033[45m'
    BACKGROUND_CYAN = '\033[46m'
    BACKGROUND_WHITE = '\033[47m'
    BACKGROUND_BRIGHT_BLACK = '\033[40;1m'
    BACKGROUND_BRIGHT_RED = '\033[41;1m'
    BACKGROUND_BRIGHT_GREEN = '\033[42;1m'
    BACKGROUND_BRIGHT_YELLOW = '\033[43;1m'
    BACKGROUND_BRIGHT_BLUE = '\033[44;1m'
    BACKGROUND_BRIGHT_MAGENTA = '\033[45;1m'
    BACKGROUND_BRIGHT_CYAN = '\033[46;1m'
    BACKGROUND_BRIGHT_WHITE = '\033[47;1m'


def enable_color() -> None:
    if os.name == "nt":  # Windows
        os.system("color")
    else:  # Linux/Macos
        pass  # Windows is the only dumb one for having to enable escape-codes


def clear() -> None:
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # Linux/Macos
        os.system("clear")


def wait_for_key() -> None:
    if os.name == "nt":  # Windows
        os.system("pause")
    else:  # Linux/Macos
        assert (False and "Internal Error: Find out how to do this on linux/macos")
