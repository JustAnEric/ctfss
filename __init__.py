if __name__ == "__main__":
    print("This is the ctfss package. It is not meant to be run directly.")
    exit(1)

import soundfile
import numpy
import os
import sys
import math
from _utils import bcolors

def i():
    print("Welcome to interactive mode. Type 'help' for a list of commands.")
    while True:
        prompt = input(f"{bcolors.GREEN}ctfss{bcolors.ENDC}> ").strip()
        args = prompt.split()
        args = [arg.lower() for i,arg in enumerate(args) if i==0]
        if args[0] == "exit":
            print("Exiting interactive mode.")
            break
        elif args[0] == "help":
            print("Available commands:")
            print("  exit - Exit interactive mode")
            print("  help - Show this help message")
            print("  make - Create a new steganograph")
            print("  decode - Decode a steganograph")
        elif args[0] == "make":
            pass
        elif args[0] == "decode":
            pass
        else:
            print(f"{bcolors.RED}Unknown command: {args[0]}{bcolors.ENDC}")

def c():
    return None

def d():
    return None