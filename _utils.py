class bcolors:  # credit: blender build scripts (expanded from that with ansi color stuff)
    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    LIGHTBLACK = "\033[90m"
    LIGHTRED = "\033[91m"
    LIGHTGREEN = "\033[92m"
    LIGHTYELLOW = "\033[93m"
    LIGHTBLUE = "\033[94m"
    LIGHTMAGENTA = "\033[95m"
    LIGHTCYAN = "\033[96m"
    LIGHTWHITE = "\033[97m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    BG_LIGHTBLACK = "\033[100m"
    BG_LIGHTRED = "\033[101m"
    BG_LIGHTGREEN = "\033[102m"
    BG_LIGHTYELLOW = "\033[103m"
    BG_LIGHTBLUE = "\033[104m"
    BG_LIGHTMAGENTA = "\033[105m"
    BG_LIGHTCYAN = "\033[106m"
    BG_LIGHTWHITE = "\033[107m"

    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    INVERT = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKE = "\033[9m"

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC, RESET = ["\033[0m"] * 2

    # dynamically generated colors :)
    @staticmethod
    def fg256(color: int) -> str:
        if not 0 <= color <= 255:
            raise ValueError("colour must be between 0 and 255")
        return f"\033[38;5;{color}m"

    @staticmethod
    def bg256(color: int) -> str:
        if not 0 <= color <= 255:
            raise ValueError("colour must be between 0 and 255")
        return f"\033[48;5;{color}m"

    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("RGB values must be between 0 and 255")
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("RGB values must be between 0 and 255")
        return f"\033[48;2;{r};{g};{b}m"

    @staticmethod
    def hex(color: str) -> str:
        color = color.lstrip("#")

        if len(color) != 6:
            raise ValueError("expected a 6-digit hex colour")

        try:
            r, g, b = (int(color[i : i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            raise ValueError("invalid hex colour") from None

        return bcolors.rgb(r, g, b)
    
__all__=["bcolors"]