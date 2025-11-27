import random
from datetime import datetime

# assign client ID
def assign_client_id():
    today = "".join([
        str(datetime.today().month),
        str(datetime.today().day),
        str(datetime.today().year)[2:]
    ])
    id = "".join([
        str(random.randint(0, 10)) for i in range(0, 4)
    ])
    return "".join(['User', today, id])

# receive messages
def receive_messages(
    client,
    colored_server_name,
    colored_client_name,
    breakers
):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("\nServer disconnected")
                break
            msg = data.decode()

            # Check if it's a file transfer
            if msg.startswith("FILE:"):
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
                print(f"{colored_client_name} ", end="", flush=True)
                continue

            # flush line before receiving, then re-prompt
            # \r\033[K flushes
            print(f"\r\033[K{colored_server_name} {msg}")
            
            if msg.lower() in breakers:
                client.close()
                break
            print(f"{colored_client_name} ", end="", flush=True)  # Re-prompt
        except:
            break

# send messages
def send_messages(
    client,
    colored_client_name,
    breakers
):
    while True:
        try:
            msg = input(f"{colored_client_name} ")
            client.sendall(msg.encode())
            if msg.lower() in breakers:
                break
        except Exception as e:
            break

# footer of instructions at bottom of client-side chat log
def footer():
    return None

# receive a file from the server
def receive_file(client, save_path):
    """Receive a file from the server"""
    # get file size
    data = client.recv(1024).decode()
    if data.startswith("ERROR"):
        print(data)
        return

    filesize = int(data.split(":")[1])

    # send acknowledgement
    client.sendall(b"READY")

    # receive file
    received = 0
    with open(save_path, "wb") as f:
        while received < filesize:
            chunk = client.recv(min(4096, filesize - received))
            if not chunk:
                break
            f.write(chunk)
            received += len(chunk)
    
    # read completion message
    client.recv(1024)
    print(f"Received {save_path} ({filesize} bytes)")
