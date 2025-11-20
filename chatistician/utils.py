import yaml
import os
import sys

# function to return unix color codes
def colors(col):
    cols = [
        ("white", "\033[30m", "\033[0m"),
        ("red", "\033[31m", "\033[0m"),
        ("green", "\033[32m", "\033[0m"),
        ("yellow", "\033[33m", "\033[0m"),
        ("blue", "\033[34m", "\033[0m"),
        ("magenta", "\033[35m", "\033[0m"),
        ("cyan", "\033[36m", "\033[0m"),
        ("white", "\033[367", "\033[0m")
    ]
    # \033[1;XXm # bold, not currently implemented
    return [x[1:] for x in cols if x[0] == col][0]

# function to get abspaths when building executable with pyinstaller
def resource_path(rel_path):
    try:
        # pyinstaller stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)
