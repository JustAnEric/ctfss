# CTFSS (Cut the FLAC Some Slack!)

> “ **heh funny pun** ”
>
> ~ developer me

I think FLAC files haven't been receiving the respect they deserve. This project converts regular files and data directly into a FLAC format.

> [!NOTE]
> ***This is more of an experiment than anything!*** I am not responsible for any data loss from this project, you use it at your own risk!
> It is definitely not an effective way to store data as the size scales, but it is a great proof-of-concept.

## Demo

You can convert files to and from CTFSS format here:

[https://ctfss.erikku.page](https://ctfss.erikku.page)

The source code for the website can be found in the [demo/](demo/) folder. The cap on this website for uploaded files is **1 MB** because of intensive compute and other implications.

## CLI

After cloning, entering the repository, and installing dependencies from `requirements.txt`, you can run the `__main__.py` file to enter the *interactive ✨* command-line interface:

```sh
# python __main__.py
~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
      ___  _____  ___  __  __                     
     / __\/__   \/ __\/ _\/ _\                    
    / /     / /\/ _\  \ \ \ \                     
   / /___  / / / /    _\ \_\ \                    
   \____/  \/  \/     \__/\__/                    
~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
|-| The FLAC Audio File Data Steganograph Tool |-|

[W] No operation specified. Defaulting to interactive mode.
Welcome to interactive mode. Type 'help' for a list of commands.
ctfss> 
```

Or you can run it directly from terminal simply for any operation:

```sh
# python __main__.py --help
~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
      ___  _____  ___  __  __                     
     / __\/__   \/ __\/ _\/ _\                    
    / /     / /\/ _\  \ \ \ \                     
   / /___  / / / /    _\ \_\ \                    
   \____/  \/  \/     \__/\__/                    
~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
|-| The FLAC Audio File Data Steganograph Tool |-|

usage: ctfss [-h] [-i INPUT] [-o OUTPUT] [{interactive,make,decode,info}]

A FLAC Audio File Data Steganograph Tool

positional arguments:
  {interactive,make,decode,info}
                        the operation

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     the input data/file (for make/decode operation)
  -o, --output OUTPUT   the output file (for make/decode operation)
```

## Supported methods of i/o

* filename input/output
* *coming later*: stdio byte input/output

You can also use this as a Python module with the `c_stream` and `d_stream` functions, if you feel somehow particularly interested in using this in a project.
