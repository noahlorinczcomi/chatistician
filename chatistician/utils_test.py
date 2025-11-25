import os
import sys
import shutil
import threading


PRINT_LOCK = threading.Lock()

def safe_print_above_footer(text, footer):
    cols, rows = shutil.get_terminal_size()

    CHAT_LINE = rows - 1      # the row just above the footer
    FOOTER_LINE = rows

    # 1. Move cursor to the chat area
    sys.stdout.write(f"\033[{CHAT_LINE};1H")
    sys.stdout.write("\033[2K")   # clear the entire chat line

    # 2. Scroll the top chat region by 1 line
    #    so older messages move upward
    sys.stdout.write("\033[S")

    # 3. After scrolling, print the new message cleanly
    sys.stdout.write(f"\033[{CHAT_LINE};1H")  # go to clean line again
    print(text, end="\n")

    # 4. Redraw footer on bottom row
    sys.stdout.write(f"\033[{FOOTER_LINE};1H")
    sys.stdout.write("\033[2K")
    sys.stdout.write(footer)
    sys.stdout.flush()

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

# function to print banner
def banner():
    ban = r"""
   ___ _  _   _ _____   ___ _____ _ _____ ___ 
  / __| || | /_\_   _| / __|_   _/_\_   _/ __|
 | (__| __ |/ _ \| |   \__ \ | |/ _ \| | \__ \
  \___|_||_/_/ \_\_|   |___/ |_/_/ \_\_| |___/                           
    """
    print(ban)

# header for server side. reminder of simulations etc.
def server_header():
    header = r"""
<- SIMULATIONS -------------------------------------------------->
  + RUN
    > format  :  !simulate {<simulation type>} <parameters>
    > example :  "!simulate {independent t test} --n1 10 --n2 30"
    > example :  "!simulate {paired t test} -n 50"
    
  + OPTIONS
    > "independent t test"
    > "paired t test"
    
  + PARAMETERS (visible only to you)
    > format  :  !simulate params {<simulation type>}
    > example :  "!simulate params {independent t test}"
    > example :  "!simulate params {paired t test}"

<- CODE --------------------------------------------------------->
  + REVIEW
    > format  :  !code review <file.extension>
    > example :  "!code review analysis.R"
    > example :  "!code review latest"
  + WRITING
    > format  :  !code write <file.extension>
    > example :  !code write mixed_model.R

<- HELP --------------------------------------------------------->
  + RUN "!help" to print this message (only visible to you)
    """
    print(header)

# client header
def client_header():
    header = """
Need help with:
  -> Power calculation? Just say: "I need a power calculation"
  -> Code review? Ask: "Can we review/write my data analysis code?"
  -> Data analysis? Ask: "Can you review my analysis?"
  -> Study design? Ask: "Help me design my study"

<- HOW TO REQUEST CODE REVIEW ---------------------------------------->
  [Example] : Type into chat: "!code review analysis.R"
  [Format]  : "!code review </local/file.extension>"

Type "quit" to end session.

Type "!help" to view this message (only visible to you).
    """
    print(header)

# function to print welcome message
def welcome(name):
    welcome_msg = f"""
    Welcome, {name}!
    
    You're connected with a professional statistician.
    """
    print(welcome_msg)
