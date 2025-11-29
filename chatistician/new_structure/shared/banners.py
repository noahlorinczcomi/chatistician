from shared import utils as shared_utils

def banner():
    """print banner"""
    ban = r"""
   ___ _  _   _ _____   ___ _____ _ _____ ___ 
  / __| || | /_\_   _| / __|_   _/_\_   _/ __|
 | (__| __ |/ _ \| |   \__ \ | |/ _ \| | \__ \
  \___|_||_/_/ \_\_|   |___/ |_/_/ \_\_| |___/                           
    """
    print(ban)
    shared_utils.persistent_footer()
    return None

def command_help(config_path="shared/config.yaml"):
    """list of commands for server side"""
    config = shared_utils.load_config(config_path)
    cmd_prefix = config['commands']['cmd_prefix']
    os_prefix = config['commands']['os_prefix']
    msg = f"""
View this help message.
+ COMMAND:  {cmd_prefix}{config['commands']['help'][0]}
+ EXAMPLE:  {cmd_prefix}{config['commands']['help'][0]}

Perform power analysis using simulation.
+ COMMAND:  {cmd_prefix}{config['commands']['simulation'][0]} {{<statistical test>}} <simulation parameters>
+ EXAMPLE:  {cmd_prefix}{config['commands']['simulation'][0]} {{paired t test}} -n 20
+ HELP:     {cmd_prefix}{config['commands']['simulation'][0]} help

Share a data analysis code file.
+ COMMAND:  {cmd_prefix}{config['commands']['share_code'][0]} <path/file.extension>
+ EXAMPLE:  {cmd_prefix}{config['commands']['share_code'][0]} ./file.R
+ HELP:     {cmd_prefix}{config['commands']['share_code'][0]} help

Review a data analysis code file.
+ COMMAND:  {cmd_prefix}{config['commands']['review_code'][0]} <path/file.extension>
+ EXAMPLE:  {cmd_prefix}{config['commands']['review_code'][0]} ./file.R
+ HELP:     {cmd_prefix}{config['commands']['review_code'][0]} help

Interact with the local system.
+ COMMAND:  {os_prefix}<UNIX command>
+ EXAMPLE:  {os_prefix}ls -la
+ EXAMPLE:  {os_prefix}tmux attach -t private_session
+ EXAMPLE:  {os_prefix}mv code/file.R ./file.R
+ HELP:     {os_prefix}help
    """
    print(msg)
    shared_utils.persistent_footer()
    return None

def simulation_help():
    msg = r"""
<- SIMULATIONS ---------------------------------------->
  + SUMMARY
    -> There are simulation tools available to you to
       perform power calculations for various statistical
       tests under different scenarios. You can perform
       these simulations by entering specific phrases
       directly into the chat.
  
  + AVAILABLE OPTIONS
    -> independent samples t-test
    -> paired samples t-test
  
  + SYNTAX
    -> !simulate {<available option>} <parameters>
  
  + EXAMPLES
    -> !simulate {independent t-test} --n1 10 --n2 30
    -> !simulate {paired t-test} -n 50
  
  + OUTPUT
    -> Simulation output is printed directly to the
       user and expert consoles and displays power
       for the test under varying effect sizes.
"""
    print(msg)
    shared_utils.persistent_footer()
    return None

def code_help_server():
    """help message for server side related to code review"""
    msg = r"""
<- CODE REVIEW ------------------------------------------->
  + SUMMARY
    -> You can review user's code by agreeing to receive
       a code file from them directly through the chat. The
       user will first request to share their code. If you
       agree, which you can indicate in the chat, you can
       review the code and send it back to them using a
       single special phrase: !review-code.
    
    + Sequence of events
      As the expert, you will:
        1. Agree to receive code file from user
        2. Run !review-code <file.extension> in the chat
        3. Enter code editor screen
        4. Save edits and/or comments to code file
        5. Leave code editor screen
        6. Run !share-code <file.extension> in the chat
      
      When you finish step 6, the edited code will also
      be automatically uploaded to Github, and both you
      and the user will be alerted of its URL.
  
  + SYNTAX
    -> !review-code <file.extension>
    -> !share-code <file.extension>
  
  + EXAMPLES
    -> !review-code linear_model.R
    -> !share-code linear_model.R
  
  + EDITING CODE
    -> After running !review-code <file.extension>, you will
       be automatically entered into a text editor with the
       code file. By default, the editor is the `micro` editor,
       which uses standard keybindings with the Cmd/Win key
       replaced with Ctrl. You leave this editor by pressing
       Cmd/Win + q
"""
    print(msg)
    shared_utils.persistent_footer()
    return None

def code_help_client():
    """help message for client side related to code"""
    msg = r"""
<- CODE REVIEW ------------------------------------------->
  + SUMMARY
    -> The statistician can review your data analysis code.
       You can share code files with them directly through 
       the chat using a special set of phrases.
  
  + SYNTAX
    -> !share-code </path/to/file.extension>
  
  + EXAMPLES
    -> !share-code analysis/linear_model.R
  
  + OUTPUT
    -> When you share your code with the expert, they will
       receive a request to download your file. Then, they
       will review it and request to send the file back to 
       you. When they send it back to you, they will also
       upload the original and edited code file to Github
       where you can see their edits and/or comments. The
       Github repo will be shared with you during the chat.
"""
    print(msg)
    shared_utils.persistent_footer()
    return None
