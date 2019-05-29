import os
import time
from config import IO_SLEEP_TIME

def clear_screen():
    if os.name == "nt":
        os.system('cls')
    elif os.name == "posix" or os.name == "mac":
        os.system("clear")

def sleep():
    time.sleep(IO_SLEEP_TIME)

# Write output to screen.
def w(str, clear=True):
    if clear: clear_screen()
    print(str)
    sleep()

def w_ln(strs, sleep=True, clear=True):
    if clear: clear_screen()
    for str in strs: print(str)
    if sleep: sleep()

# Clear screen & Read string as an input
def r_str(str, strarray=None, min=None, max=None, clear=True, error_msg=None):
    if clear: clear_screen()
    valid = False
    result = ""
    while not valid:
        if strarray:
            for item in strarray: print(item)
        result = input(str + ": ")
        if not min and not max: valid = True
        elif (min and not max): valid = True if len(result) >= min else False
        elif (max and not min): valid = True if len(result) <= max else False
        else: valid = True if len(result) >= min and len(result) <= max else False
        if not valid: 
            op = error_msg if error_msg else "Invalid input."
            w(op)
            clear_screen()
    return result

def r_int(str, strarray=None, min=None, max=None, clear=True, error_msg=None):
    valid = False
    result = None
    while not valid:
        try: 
            if clear: clear_screen()
            if strarray:
                for item in strarray: print(item)
            result = int(input(str + ": "))
            if not min and not max: valid = True
            elif (min and not max): valid = True if result >= min else False
            elif (max and not min): valid = True if result <= max else False
            else: valid = True if result >= min and result <= max else False
            if not valid: 
                op = error_msg if error_msg else "Invalid input."
                w(op)
        except ValueError:
            w("Please input a valid integer.")
    return result

