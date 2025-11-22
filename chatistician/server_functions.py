import os
import subprocess

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
            # flush line before receiving, then re-prompt
            # \r\033[K flushes
            print(f"\r\033[K{colored_client_name} {msg}")
            print(f"{colored_server_name} ", end="", flush=True) # re-prompt
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
    ttest_subs = ['t-test', 't test']
    is_ttest = any(s in sim_name for s in ttest_subs)
    paired_subs = ['paired', 'pair', 'repeated', 'matched']
    is_paired = any(s in sim_name for s in paired_subs)
    
    # other simulation types ...
    available_scripts = os.listdir('power_analysis')
    script = f"simulation type not found. Options are: {', '.join(available_scripts)}"
    if is_ttest and not is_paired:
        script = 'independent_t-test.R'
    elif is_ttest and is_paird:
        script = 'paired_t-test.R'
    return script

# function to parse messages before sending/running
def parse_msg(
    msg,
    cmd_prefix='$',
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
    if msg[0] != cmd_prefix:
        parsed = {'message_type': 'chat', 'message': msg}
    # then user wants to run a command
    elif msg.split(" ")[1].lower() in sim_commands:
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
    elif msg.split(" ")[1].lower() in file_commands:
        print('file sharing not implemented yet')
        parsed = {}
    
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
                conn.sendall(sim_result.encode())
            #conn.sendall(msg.encode())
            if msg.lower() in breakers:
                conn.close()
                break
        except:
            break
