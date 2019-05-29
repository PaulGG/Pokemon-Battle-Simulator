#!/usr/bin/python3

# python library contents

from pathlib import Path
import json
import pokepy

# custom library contents

from functions import io, begin

def main():
    io.w("Welcome to Pokemon!")
    save = Path("./save.json")
    # if json file does not exist, run first time setup
    if not save.is_file():
        init()

def init():
    name = io.r_str("Please enter your name (1 - 20 characters)", min=1, max=20,  
        error_msg="Your name must have 1 to 20 characters.")
    starter = begin.choose_starter()

if __name__ == "__main__": 
    main()