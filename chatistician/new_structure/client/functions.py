import os
from shared import utils as shared_utils

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Message handling

# receive messages
def receive_msg(
    client,
    colored_server_name,
    colored_client_name,
    breakers,
    file_prefix="FILE:"
):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("\nServer disconnected")
                break
            msg = data.decode()

            # Check if it's a file transfer
            if msg.startswith(file_prefix):
                receive_file(data, msg, client)
                print(f"{colored_client_name} ", end="", flush=True)
                continue
            
            # flush line before receiving, then re-prompt
            # \r\033[K flushes
            print(f"\r\033[K{colored_server_name} {msg}")
            shared_utils.persistent_header() # keeps help header at top of terminal
            
            if msg.lower() in breakers:
                client.close()
                break
            print(f"{colored_client_name} ", end="", flush=True)  # Re-prompt
        except:
            break

# send messages
def send_msg(
    client,
    colored_client_name,
    breakers
):
    while True:
        try:
            msg = input(f"{colored_client_name} ")
            # check if wants to send a file
            if msg.startswith("!get"):
                filename = msg.split(" ")[1]
                send_file(client, filename)
            else:
                client.sendall(msg.encode())
            if msg.lower() in breakers:
                break
            shared_utils.persistent_header() # keeps help header at top of terminal
        except Exception as e:
            break

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# File handling

# receive a file from the server
def receive_file(data, msg, client):
    parts = msg.split(":", 3)
    filename = parts[1]
    filesize = int(parts[2])
    
    # Receive the file content
    file_data = data[len(f"FILE:{filename}:{filesize}:"):]
    remaining = filesize - len(file_data)
    
    while remaining > 0:
        chunk = client.recv(min(4096, remaining))
        file_data += chunk
        remaining -= len(chunk)
    
    # Save file
    with open(filename, 'wb') as f:
        f.write(file_data)
    
    print(f"\r\033[KReceived file: {filename} ({filesize} bytes)")

# send file over socket
def send_file(client, filepath):
    """Send a file to the client"""
    if not os.path.exists(filepath):
        print("ERROR: File not found")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    
    # Send file header
    client.sendall(f"FILE:{filename}:{filesize}:".encode())
    
    # Send file content immediately
    with open(filepath, "rb") as f:
        client.sendall(f.read())
    
    print(f"Sent {filepath}")