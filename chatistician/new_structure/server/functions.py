import os
from shared import utils as shared_utils
from shared import simulations

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Message handling

# receive message
def receive_msg(
    conn,
    colored_client_name,
    colored_server_name,
    breakers,
    file_prefix="FILE:"
):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"\n{colored_client_name} disconnected")
                break # out of while loop
            msg = data.decode()

            # Check if it's a file transfer
            if msg.startswith(file_prefix):
                receive_file(data, msg, conn)
                print(f"{colored_server_name} ", end="", flush=True)
                continue

            # flush line before sending
            # \r\033[K flushes
            print(f"\r\033[K{colored_client_name} {msg}")
            # shared_utils.persistent_header() # print help header after sending message
            shared_utils.persistent_footer() # print help footer after sending message

            # re-prompt the server
            print(f"{colored_server_name} ", end="", flush=True)
            
            if msg.lower() in breakers:
                conn.close()
                break
        except OSError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

# send message
def send_msg(
    conn,
    colored_server_name,
    breakers,
    config_path
):
    while True:
        try:
            msg = input(f"{colored_server_name}")
            if msg == "":
                conn.sendall(msg.encode())
                continue
            parsed_msg = shared_utils.parse_msg(msg, config_path)
            # make sure we know what message is trying to sent
            if parsed_msg is None:
                # will happen when server just wants to print
                # a help message for themselves to see.
                continue
            elif parsed_msg['message_type'] == 'chat':
                conn.sendall(msg.encode())
            elif parsed_msg['message_type'] == 'simulation':
                sim_result = simulations.run_simulation(
                    script=parsed_msg['script'],
                    args=parsed_msg['args']
                )
                print(sim_result)
                conn.sendall(sim_result.encode())
            elif parsed_msg['message_type'] == 'file':
                filename = parsed_msg['filename']
                send_file(conn, filename)
            
            # shared_utils.persistent_header() # print help header after sending message
            shared_utils.persistent_footer() # print help footer after sending message
            
            if msg.lower() in breakers:
                conn.close()
                break
        except OSError:
            break
        except EOFError:
            break
        except KeyboardInterrupt:
            break

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# File handling
# receive a file from the client
def receive_file(data, msg, conn):
    parts = msg.split(":", 3)
    filename = parts[1]
    filesize = int(parts[2])
    
    # Receive the file content
    file_data = data[len(f"FILE:{filename}:{filesize}:"):]
    remaining = filesize - len(file_data)
    
    while remaining > 0:
        chunk = conn.recv(min(4096, remaining))
        file_data += chunk
        remaining -= len(chunk)
    
    # Save file
    with open(filename, 'wb') as f:
        f.write(file_data)
    
    print(f"\r\033[KReceived file: {filename} ({filesize} bytes)")
    # shared_utils.persistent_header() # print help header after sending message
    shared_utils.persistent_footer() # print help footer after sending message

# receive a file from the client
def receive_file(data, msg, conn):
    parts = msg.split(":", 3)
    filename = parts[1]
    filesize = int(parts[2])
    
    # Receive the file content
    file_data = data[len(f"FILE:{filename}:{filesize}:"):]
    remaining = filesize - len(file_data)
    
    while remaining > 0:
        chunk = conn.recv(min(4096, remaining))
        file_data += chunk
        remaining -= len(chunk)
    
    # Save file
    with open(filename, 'wb') as f:
        f.write(file_data)
    
    print(f"\r\033[KReceived file: {filename} ({filesize} bytes)")
    # shared_utils.persistent_header() # print help header after sending message
    shared_utils.persistent_footer() # print help footer after sending message

# send file over socket
def send_file(conn, filepath):
    """Send a file to the client"""
    if not os.path.exists(filepath):
        print("ERROR: File not found")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    
    # Send file header
    conn.sendall(f"FILE:{filename}:{filesize}:".encode())
    
    # Send file content immediately
    with open(filepath, "rb") as f:
        conn.sendall(f.read())
    
    print(f"Sent {filepath}")
    # shared_utils.persistent_header() # print help header after sending message
    shared_utils.persistent_footer() # print help footer after sending message
