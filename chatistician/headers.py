# function to print masthead/banner
def masthead():
    mh = """
╔══════════════════════════════════════════════════════════════╗
║           Chatistician: Rapid Statistical Advice             ║
╚══════════════════════════════════════════════════════════════╝
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
    [+ === SIMULATIONS =============================================== +]
      [REQUEST]
        "independent t test"
        "paired t test"
    


    [+ === CODE ====================================================== +]
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
    - Power calculation? Just ask: "I need a power calculation"
    - Study design? Ask: "Help me design my study"  
    - Data analysis? Ask: "Can you review my analysis?"
    - Code review? Ask: "Can we review/write my data analysis code?"
    
    Type 'quit' to end session.
    """
    print(welcome_msg)

# function to print section headers
def print_section_header(title, size=78):
    print("\n" + "─" * size)
    print(f"  {title}")
    print("─" * size + "\n")
