import os
import sys
import yaml
import shutil
from datetime import datetime
import subprocess
from server import utils as server_utils
from shared import banners as shared_banners

def persistent_header(
    config_path="shared/config.yaml",
    fg_color=30,
    bg_color=42
):
    """
    Print header whenever a message is sent or received.
    This code gets the current cursor position, goes to
    the top line and prints the header, and jumps back
    to the original cursor position. it is ran after
    messages are sent and received.
    """
    # load config file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)


    # Get terminal width
    cols, _ = shutil.get_terminal_size()
    command_prefix = config['commands']['prefix']
    text = "Commands: "
    for val in config['commands'].values():
        if val == command_prefix:
            continue
        text = text + f"{command_prefix}{val[0]}, "

    text = text[:-2] # remove trailing ", "
    text = text + r". Try '!{command} help' anytime."

    # construct color string (foreground + background)
    color_seq = f"\033[{fg_color}m" + f"\033[{bg_color}m"
    reset_seq = "\033[0m"

    # In case the header doesn't cover the entire width
    # of the terminal and you want a background color,
    # pad the header text to cover the entire width
    dt = datetime.now().strftime("%Y-%m-%d")
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

def colors(col):
    """return unix color codes"""
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

def load_config(filepath):
    """load config file"""
    config_path = resource_path(filepath)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# function to parse messages before sending/running
def parse_msg(msg, config_path):
    """
    The idea is that some messages from the server 
    will be chats, and others will be commands to
    execute other commands/files. I want to make sure
    I know what type of information the message intends
    to send before sending. This function returns the
    parsed message and its type. It does not actually
    send the message or execute any commands
    """
    if len(msg) == 0:
        return {'message_type': 'chat', 'message': msg}

    # record config file metadata
    config = load_config(config_path)
    cmd_prefix = config['commands']['prefix']
    help_commands = config['commands']['help']
    sim_commands = config['commands']['simulation']
    file_send_commands = config['commands']['file_send']
    file_edit_commands = config['commands']['file_edit']

    clean_msg = msg.lstrip() # remove prefixing spaces

    is_cmd = clean_msg[0] == cmd_prefix
    prefix = clean_msg.split(" ")[0].lower()
    is_sim = prefix[1:] in sim_commands
    is_file = prefix[1:] in file_send_commands
    is_help = prefix[1:] in help_commands
    is_editor = prefix[1:] in file_edit_commands

    # then user wants to run a command
    if not is_cmd:
        return {
            'message_type': 'chat',
            'message': msg,
            'script': None,
            'args': None
        }
    if is_sim:
        # else, user wants to perform a simulation. The
        # message itself will contain the simulation
        # parameters if they want to perform a simulation
        script, args = server_utils.parse_simulation(msg)
        parsed = {
            'message_type': "simulation",
            'message': None,
            'script': f"power_analysis/{script}",
            'args': args
        }
        # make sure the expert didn't just want to see the
        # flags/arguments/params of the simulation function
        if clean_msg.split(" ")[1].lower() in ['params', 'parameters']:
            parsed['message_type'] = "params"
            parsed['args'] = '--help' # replaces 'args' entry
        return parsed
    
    if is_file:
        if len(clean_msg.split(" ")) > 1:
            filename = clean_msg.split(" ", 1)[1]
        else:
            filename = ""
        return {
            "message_type": "file",
            "message": None,
            "script": None,
            "filename": filename
        }

    if is_help:
        shared_banners.server_header()
        return {
            "message_type": None,
            "message": None,
            "script": None,
            "filename": None
        }

    if is_editor:
        # msg[1:] takes off the cmd_prefix (e.g., '!')
        subprocess.run(clean_msg[1:], text=True, shell=True)
        return {
            "message_type": None,
            "message": None,
            "script": None,
            "filename": None
        }
    
    # if made it this far, not a chat, not a sim or
    # file command, so just return exact message with 
    # a prefix that it was command-ambiguous
    new_msg = f"[COMMAND-AMBIGUOUS] {clean_msg}"
    parsed = {'message_type': 'chat', 'message': new_msg}
    return parsed

