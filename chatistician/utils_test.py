import os
import sys
import shutil

def init_footer_area():
    cols, rows = shutil.get_terminal_size()
    # Set scrolling region: lines 1 .. rows-1 scroll
    # Bottom line (rows) is protected
    sys.stdout.write(f"\033[1;{rows-1}r")
    sys.stdout.flush()

def draw_footer(text="example footer"):
    cols, rows = shutil.get_terminal_size()

    # Save cursor pos
    sys.stdout.write("\0337")

    # Write footer on bottom line
    sys.stdout.write(f"\033[{rows};1H")  # bottom row
    sys.stdout.write("\033[2K")          # clear entire line
    sys.stdout.write(text)

    # Restore cursor
    sys.stdout.write("\0338")
    sys.stdout.flush()

def print_client_message(client_msg, colored_client_name, colored_server_name):
    # Save cursor (where server user is typing)
    sys.stdout.write("\0337")

    # Move cursor to just above server prompt
    sys.stdout.write("\033[F")  # move up 1 line
    sys.stdout.write("\033[2K") # clear entire line
    sys.stdout.write(f"{colored_client_name} {client_msg}\n")

    # Restore cursor to server prompt line
    sys.stdout.write("\0338")
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
