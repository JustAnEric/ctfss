import sys

from __init__ import i, c, d, cc, c_stream, d_stream
from _utils import bcolors
import argparse


def sb():
    info_text = "|-| The FLAC Audio File Data Steganograph Tool |-|"
    info_text_real = f"{bcolors.HEADER}{info_text}{bcolors.ENDC}"
    info_text_len = len(info_text)

    banner_lines = [
        "      ___  _____  ___  __  __                     ",
        "     / __\\/__   \\/ __\\/ _\\/ _\\                    ",
        "    / /     / /\\/ _\\  \\ \\ \\ \\                     ",
        "   / /___  / / / /    _\\ \\_\\ \\                    ",
        "   \\____/  \\/  \\/     \\__/\\__/                    ",
    ]  # made from an ascii website and padded manually, could'a used a text file or smth
    gradient_lines = []
    starting_color = (214, 112, 214)
    ending_color = (188, 63, 188)
    # from top to bottom

    for y, banner_line in enumerate(banner_lines):
        gradient_line = ""

        factor = y / (len(banner_lines) - 1)

        r = int(starting_color[0] + (ending_color[0] - starting_color[0]) * factor)
        g = int(starting_color[1] + (ending_color[1] - starting_color[1]) * factor)
        b = int(starting_color[2] + (ending_color[2] - starting_color[2]) * factor)

        color = bcolors.bg_rgb(r, g, b)
        fgcol = bcolors.hex("#000000")

        for char in banner_line:
            gradient_line += f"{color}{fgcol}{char}"

        gradient_lines.append(gradient_line + bcolors.ENDC)

    return f"""{bcolors.BG_MAGENTA}{'~=' * (info_text_len//2)}{bcolors.ENDC+bcolors.HEADER+bcolors.BOLD}
{'\n'.join(gradient_lines)}{bcolors.ENDC}
{bcolors.UNDERLINE+bcolors.BG_MAGENTA}{'~=' * (info_text_len//2)}{bcolors.ENDC}
{info_text_real}\n"""


def vi():
    vt = "Version: 0.1.0"
    l = "~="
    ll = len(l)
    wincolor = bcolors.BG_BLUE
    return f"""{wincolor}{l * 20}{bcolors.ENDC}
{wincolor} {bcolors.ENDC+bcolors.HEADER+bcolors.BOLD}{vt}{' ' * ((20 * ll) - len(vt)-2)}{bcolors.ENDC+wincolor} {bcolors.ENDC}
{bcolors.UNDERLINE+wincolor}{l * 20}{bcolors.ENDC}
"""


if __name__ == "__main__":
    print(sb())

    parser = argparse.ArgumentParser(
        prog="ctfss",
        description="A FLAC Audio File Data Steganograph Tool",
    )

    parser.add_argument(
        "operation",
        help="the operation",
        choices=["interactive", "make", "decode", "info"],
        nargs="?",
    )

    parser.add_argument(
        "-i",
        "--input",
        help="the input data/file (for make/decode operation)",
        required=False,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="the output file (for make/decode operation)",
        required=False,
    )

    args = parser.parse_args()

    if not args.operation:
        print(
            f"{bcolors.BG_YELLOW}W{bcolors.ENDC} {bcolors.WARNING}No operation specified. Defaulting to interactive mode.{bcolors.ENDC}"
        )
        args.operation = "interactive"

    if args.operation == "interactive":
        i()

    elif args.operation == "make":
        input_file = args.input
        output_file = args.output

        if not input_file:
            input_file = sys.stdin.buffer
            print("Reading from stdin...")
        else:
            input_file = open(input_file, "rb")

        if not output_file:
            raise ValueError("c_stream currently requires an output file")

        try:
            for percent in c_stream(input_file, output_file):
                sys.stdout.write(
                    f"\r{bcolors.CYAN}Progress: {percent:.2f}%{bcolors.ENDC}"
                )
                sys.stdout.flush()
            print(
                f"\n{bcolors.GREEN}Successfully created steganograph: {output_file}{bcolors.ENDC}"
            )
        finally:
            if input_file is not sys.stdin.buffer:
                input_file.close()

    elif args.operation == "decode":
        input_file = args.input
        output_file = args.output

        if not input_file:
            input_file = sys.stdin.buffer
            print("Reading from stdin...")
        else:
            input_file = open(input_file, "rb")

        if not output_file:
            raise ValueError("d_stream currently requires an output file")
        else:
            output_file = open(output_file, "wb")

        try:
            for percent in d_stream(input_file, output_file):
                sys.stdout.write(
                    f"\r{bcolors.CYAN}Progress: {percent:.2f}%{bcolors.ENDC}"
                )
                sys.stdout.flush()
            print(
                f"\n{bcolors.GREEN}Successfully decoded steganograph: {output_file}{bcolors.ENDC}"
            )
        finally:
            if input_file is not sys.stdin.buffer:
                input_file.close()

    elif args.operation == "info":
        print(vi())
