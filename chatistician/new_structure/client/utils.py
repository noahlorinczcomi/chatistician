import random
from datetime import datetime
import shutil
import sys

def persistent_header(
    fg_color=30,
    bg_color=47
):
    """
    Print header whenever a message is sent or received.
    This code gets the current cursor position, goes to
    the top line and prints the header, and jumps back
    to the original cursor position. it is ran after
    messages are sent and received.
    """
    # Get terminal width
    cols, _ = shutil.get_terminal_size()

    # construct color string (foreground + background)
    color_seq = f"\033[{fg_color}m" + f"\033[{bg_color}m"
    reset_seq = "\033[0m"

    # In case the header doesn't cover the entire width
    # of the terminal and you want a background color,
    # pad the header text to cover the entire width
    dt = datetime.now().strftime("%Y-%m-%d")
    text = f"Type !help for commands"
    padded_text = text.ljust(cols)

    # save cursor position then move to top-left position
    sys.stdout.write("\033[s")      # save cursor position
    sys.stdout.write("\033[H")      # move to top-left position
    sys.stdout.write("\033[2K")     # clear top-left line

    # print persistent header
    sys.stdout.write(f"{color_seq}{padded_text}{reset_seq}\n")

    # put cursor back where it was
    sys.stdout.write("\033[u")
    sys.stdout.flush()

# assign client ID
def assign_client_id():
    today = "".join([
        str(datetime.today().month),
        str(datetime.today().day),
        str(datetime.today().year)[2:]
    ])
    id = "".join([
        str(random.randint(0, 10)) for i in range(0, 4)
    ])
    return "".join(['User', today, id])

# function to print welcome message for client
def welcome(name):
    welcome_msg = f"""
    Welcome, {name}!
    
    You're connected with a professional statistician.
    """
    print(welcome_msg)
