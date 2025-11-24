import os
import subprocess

def get_terminal_height():
    return os.get_terminal_size().lines

def draw_footer(session_info="example footer"):
    """Draw footer at bottom of terminal"""
    # Save cursor position, move to bottom, draw footer, restore cursor
    footer_text = f"Session: {session_info}"
    print(f"\033[s", end="")  # Save cursor position
    print(f"\033[{get_terminal_height()};0H", end="")  # Move to bottom row
    print(f"\033[K{footer_text}", end="")  # Clear line and print footer
    print(f"\033[u", end="", flush=True)  # Restore cursor position

# receive message
def receive_msg(
    conn,
    colored_client_name,
    colored_server_name,
    breakers
):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"\n{colored_client_name} disconnected")
                break # out of while loop
            msg = data.decode()
            # flush line before receiving
            print(f"\r\033[K{colored_client_name} {msg}")
            
            print("\r\033[K")
            draw_footer()

            # re-prompt for client
            print(f"{colored_server_name} ", end="", flush=True)
            if msg.lower() in breakers:
                conn.close()
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# function to run simulation (R script) from within chat
def run_simulation(script, args):
    cmd = f"Rscript {script} {args}"
    run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return run.stdout

# function to read simulation description and return R script name
def match_sim_to_script(sim_name):
    sim_name = sim_name.lower()
    # T-tests
    ttest_subs = ['t-test', 't test', ' t']
    is_ttest = any(s in sim_name for s in ttest_subs)
    paired_subs = ['paired', 'pair', 'repeated', 'matched']
    is_paired = any(s in sim_name for s in paired_subs)
    
    # other simulation types ...
    available_scripts = os.listdir('power_analysis')
    script = f"ERROR: simulation type not found. Options are: {', '.join(available_scripts)}"
    if is_ttest and not is_paired:
        script = 'independent_t-test.R'
    elif is_ttest and is_paired:
        script = 'paired_t-test.R'
    return script

# function to parse messages before sending/running
def parse_msg(
    msg,
    cmd_prefix='!',
    sim_commands=['simulate', 'simulation'],
    file_commands=['get', 'download']
):
    """
    The idea is that some messages from the server 
    will be chats, and others will be commands to
    execute other commands/files. I want to make sure
    I know what type of information the message intends
    to send before sending. This function returns the
    parsed message and its type. It does not actually
    send the message or execute any commands
    """
    is_cmd = msg[0] == cmd_prefix
    prefix = msg.split(" ")[0].lower()
    is_sim = prefix[1:] in sim_commands
    is_file = prefix[1:] in file_commands
    if len(msg) == 0 or not is_cmd:
        parsed = {'message_type': 'chat', 'message': msg}
    # then user wants to run a command
    elif is_cmd and is_sim:
        # else, user wants to perform a simulation. The
        # message itself will contain the simulation
        # parameters if they want to perform a simulation
        script_start = msg.index('{') + 1
        script_end = msg.index('}')
        sim_type = msg[script_start:script_end]
        script = match_sim_to_script(sim_type)
        args = msg[(script_end + 2):]
        parsed = {
            'message_type': 'simulation',
            'script': f"power_analysis/{script}",
            'args': args
        }
        # make sure the expert didn't just want to see the
        # flags/arguments/params of the simulation function
        if msg.split(" ")[1].lower() in ['params', 'parameters']:
            parsed['args'] = '--help' # replaces
    elif is_cmd and is_file:
        print('file sharing not implemented yet')
        parsed = {}
    else:
        # not a chat, not a sim or file command, so just
        # return exact message with a prefix that it was
        # command-ambiguous
        new_msg = f"[COMMAND-AMBIGUOUS] {msg}"
        parsed = {'message_type': 'chat', 'message': new_msg}
    return parsed

# send message
def send_msg(
    conn,
    colored_server_name,
    breakers
):
    while True:
        try:
            msg = input(f"{colored_server_name} ")
            parsed_msg = parse_msg(msg)
            # make sure we know what message is trying to sent
            if parsed_msg['message_type'] == 'chat':
                conn.sendall(msg.encode())
            elif parsed_msg['message_type'] == 'simulation':
                sim_result = run_simulation(
                    script=parsed_msg['script'],
                    args=parsed_msg['args']
                )
                print(sim_result)
                conn.sendall(sim_result.encode())
            #conn.sendall(msg.encode())
            if msg.lower() in breakers:
                conn.close()
                break
        except:
            break
