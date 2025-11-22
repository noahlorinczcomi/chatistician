
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
def run_simulation(script, **kwargs):
    cmd = [
        f"Rscript {script} {kwargs}"
    ]
    subprocess.run(cmd)

# function to parse messages before sending/running
def server_msg_parser(
    conn,
    msg,
    colored_server_name,
    cmd_prefix='$',
    sim_commands=['simulate', 'simulation'],
    file_commands=['get', 'download']
):
    """
    The idea is that some messages from the server 
    will be chats, and others will be commands to
    execute other commands/files. I want to make sure
    I know what type of information the message intends
    to send before sending
    """
    if msg[0] != cmd_prefix:
        send_msg(conn, name, breakers)
    elif msg[0] in sim_commands:
        # else, user wants to perform a simulation. The
        # message itself will contain the simulation
        # parameters if they want to perform a simulation
        kwargs = " ".join(msg.split()[3:])
        run_simulation(script, kwargs)
    elif msg[0] in file_commands:
        # don't have a solution for this yet
        pass

# send message
def send_msg(
    conn,
    colored_server_name,
    breakers
):
    while True:
        try:
            msg = input(f"{colored_server_name} ")
            # make sure we know what message is trying to sent
            server_msg_parser(
                conn,
                msg,
                colored_server_name
            )
            # check if message is for an R script
            if msg[0] == ':' and 
            conn.sendall(msg.encode())
            if msg.lower() in breakers:
                conn.close()
                break
        except:
            break
