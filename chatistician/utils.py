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

# function to print masthead/banner
def masthead():
    mh = r"""
   ___ _  _   _ _____   ___ _____ _ _____ ___ 
  / __| || | /_\_   _| / __|_   _/_\_   _/ __|
 | (__| __ |/ _ \| |   \__ \ | |/ _ \| | \__ \
  \___|_||_/_/ \_\_|   |___/ |_/_/ \_\_| |___/                           
    """
    print(mh)

# header for server side. reminder of simulations etc.
def server_header():
    header = """
    [+ === SIMULATIONS ================================================ +]
      [RUN]
        [format]   !simulate {<simulation type>} <parameters>
        [example]  !simulate {independent t test} --n1 10 --n2 30
        [example]  !simulate {paired t test} -n 50
     
      [OPTIONS]
        "independent t test", "paired t test"
     
      [PARAMETERS] (visible only to you)
        [format]   !simulate params {<simulation type>}
        [example]  !simulate params {independent t test}
        [example]  !simulate params {paired t test}


    [+ === CODE ======================================================= +]
      [REVIEW]
        [format]   !review code <file_name.extentsion>
        [example]  !review code analysis.R
        [example]  !review code latest
    
    """
    print(header)

# client header
def client_header():
    header = """
    [+ SIMULATIONS =============================================== +]
       [REQUEST]
          "independent t test"
          "paired t test"

    [+ CODE ====================================================== +]
       [REVIEW] (you must add the ":")
         [format]   !review code <file_name.extension>
         [example]  !review code analysis.R
    
    """
    print(header)

# function to print welcome message
def welcome(name):
    welcome_msg = f"""
    Welcome, {name}!
    
    You're connected with a professional statistician.
    
    Need help with:
    - Power calculation? Just say: "I need a power calculation"
    - Code review? Ask: "Can we review/write my data analysis code?"
    - Data analysis? Ask: "Can you review my analysis?"
    - Study design? Ask: "Help me design my study"
    
    Type 'quit' to end session.
    """
    print(welcome_msg)
