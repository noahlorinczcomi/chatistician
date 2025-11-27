def banner():
    """print banner"""
    ban = r"""
   ___ _  _   _ _____   ___ _____ _ _____ ___ 
  / __| || | /_\_   _| / __|_   _/_\_   _/ __|
 | (__| __ |/ _ \| |   \__ \ | |/ _ \| | \__ \
  \___|_||_/_/ \_\_|   |___/ |_/_/ \_\_| |___/                           
    """
    print(ban)

def server_header():
    """header for server side. reminder of simulations etc."""
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

def client_header():
    """client header"""
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
