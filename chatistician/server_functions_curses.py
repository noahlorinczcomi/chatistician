import os
import subprocess
import utils
import threading
import curses
from datetime import datetime

# global state for curses windows
chat_win = None
footer_win = None
messages = []
lock = threading.Lock()

# draw footer
def draw_footer(status_text="Connected"):
    """draw the persistent footer with `status_text`"""
    if footer_win is None:
        return

    with lock:
        parent_height, parent_weight = curses.LINES, curses.COLS
        timestamp = datetime.now().strftime("%H:%M:%D")
        status = f"{status_text} | {timestamp}"

        footer_win.clear()
        footer_win.attron(curses.A_REVERSE)
        footer.win_addstr(0, 0, status.ljust(parent_width - 1))
        footer.win_attroff(curses.A_REVERSE)
        footer.win_refresh()

# draw chat in top window
def draw_chat():
    """Redraw all chat messages"""
    if chat_win is None:
        return
    
    with lock:
        chat_win.clear()
        height, width = chat_win.getmaxyx()

        # display all messages (can scroll up)
        for i, msg in enumerate(messages):
            try:
                chat_win.addstr(i, 0, msg[:width-1])
            except curses.error:
                pass
        
        # scroll to latest messages
        current_line = max(0, len(messages) - height)
        chat_win.refresh(current_line, 0, 0, 0, height - 1, width - 1)

def add_message(msg):
    """add message to chat window"""
    with lock:
        messages.append(msg)
    draw_chat()


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
    file_commands=['get', 'download'],
    help_commands=['help', 'help me'],
    editor_commands=['micro', 'nano', 'vim']
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
    if len(msg) == 0:
        return {'message_type': 'chat', 'message': msg}

    is_cmd = msg[0] == cmd_prefix
    prefix = msg.split(" ")[0].lower()
    is_sim = prefix[1:] in sim_commands
    is_file = prefix[1:] in file_commands
    is_help = prefix[1:] in help_commands
    is_editor = prefix[1:] in editor_commands

    # then user wants to run a command
    if not is_cmd:
        return {'message_type': 'chat', 'message': msg}
    if is_sim:
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
        return parsed
    
    if is_file:
        print('file sharing not implemented yet')
        return {}

    if is_help:
        utils.server_header()
        return None

    if is_editor:
        # msg[1:] takes off the cmd_prefix (e.g., '!')
        subprocess.run(msg[1:], text=True, shell=True)
    
    # if mdae it this far, not a chat, not a sim or
    # file command, so just return exact message with 
    # a prefix that it was command-ambiguous
    new_msg = f"[COMMAND-AMBIGUOUS] {msg}"
    parsed = {'message_type': 'chat', 'message': new_msg}
    return parsed


# send message - curses version
def send_msg_curses(
    conn,
    colored_server_name,
    breakers
):
    """Read input directly from chat window"""
    scroll_pos = 0  # Track scroll position
    
    while True:
        try:
            # Update footer
            draw_footer("Connected | PgUp/PgDn to scroll")
            
            # Get terminal height for scrolling
            height = curses.LINES - 1
            
            # Use curses to get a character
            with lock:
                # Position input at bottom of visible area
                input_line = min(len(messages), height - 1)
                chat_win.move(len(messages), 0)
            
            # Enable echo and get string
            curses.echo()
            curses.curs_set(1)
            
            # Set timeout for input to allow scroll handling
            chat_win.timeout(100)
            
            try:
                msg_bytes = chat_win.getstr()
                msg = msg_bytes.decode('utf-8').strip()
            except:
                # Timeout or error, continue loop
                curses.noecho()
                continue
            
            curses.noecho()
            
            if msg == "":
                conn.sendall(msg.encode())
                continue
                
            parsed_msg = parse_msg(msg)
            
            if parsed_msg is None:
                continue
            elif parsed_msg['message_type'] == 'chat':
                add_message(f"{colored_server_name} {msg}")
                conn.sendall(msg.encode())
            elif parsed_msg['message_type'] == 'simulation':
                add_message(f"{colored_server_name} Running simulation...")
                sim_result = run_simulation(
                    script=parsed_msg['script'],
                    args=parsed_msg['args']
                )
                # Add each line of simulation output
                for line in sim_result.split('\n'):
                    if line.strip():
                        add_message(line)
                conn.sendall(sim_result.encode())
            
            # Re-prompt
            add_message(f"{colored_server_name} ")
            
            if msg.lower() in breakers:
                conn.close()
                break
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            add_message(f"Send error: {e}")
            break

def run_chat_with_curses(stdscr, conn, colored_client_name, colored_server_name, breakers):
    """Main curses setup and event loop"""
    global chat_win, footer_win, messages
    
    # Setup
    curses.curs_set(1)
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Create windows - chat takes all but bottom row
    chat_height = height - 1
    # Use a pad instead of window for scrolling - make it large enough for lots of messages
    chat_win = curses.newpad(10000, width)  # 10000 lines should be plenty
    footer_win = curses.newwin(1, width, height - 1, 0)
    
    chat_win.scrollok(True)
    chat_win.keypad(True)
    
    # Initial messages
    messages = [
        "=== Chat Server Started ===",
        "Type your message and press Enter.",
        "Use ! prefix for commands.",
        f"Connected to {colored_client_name}",
        f"{colored_server_name} "
    ]
    
    draw_chat()
    draw_footer("Connected")
    
    # Start receive thread
    recv_thread = threading.Thread(
        target=receive_msg,
        args=(conn, colored_client_name, colored_server_name, breakers),
        daemon=True
    )
    recv_thread.start()
    
    # Run send loop (blocking, handles input)
    send_msg_curses(conn, colored_server_name, breakers)

def start_curses_server(conn, colored_client_name, colored_server_name, breakers):
    """Entry point to start curses UI"""
    curses.wrapper(
        run_chat_with_curses,
        conn,
        colored_client_name,
        colored_server_name,
        breakers
    )

# send message
def send_msg(
    conn,
    colored_server_name,
    breakers
):
    while True:
        try:
            msg = input(f"{colored_server_name}")
            if msg == "":
                conn.sendall(msg.encode())
                continue
            parsed_msg = parse_msg(msg)
            # make sure we know what message is trying to sent
            if parsed_msg is None:
                # will happen when server just wants to print
                # a help message for themselves to see.
                continue
            elif parsed_msg['message_type'] == 'chat':
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
