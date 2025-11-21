import yaml
import os
import struct
import sys

# function to return unix color codes
def colors(col):
    cols = [
        ("white", "\033[30m", "\033[0m"),
        ("red", "\033[31m", "\033[0m"),
        ("green", "\033[32m", "\033[0m"),
        ("yellow", "\033[33m", "\033[0m"),
        ("blue", "\033[34m", "\033[0m"),
        ("magenta", "\033[35m", "\033[0m"),
        ("cyan", "\033[36m", "\033[0m"),
        ("white", "\033[367", "\033[0m")
    ]
    # \033[1;XXm # bold, not currently implemented
    return [x[1:] for x in cols if x[0] == col][0]

# function to get abspaths when building executable with pyinstaller
def resource_path(rel_path):
    try:
        # pyinstaller stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

# function to send file from client to server
def send_file(client_socket, filepath):
    try:
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)
        print(f"Sending {filename} ({file_size/1e6}Mb)")

        # send message indicating file incoming
        client_socket.send(b'F')
        # send filename length and filename
        filename_bytes = filename.encode()
        client_socket.send(struct.pack("I", len(filename_bytes)))
        client_socket.send(filename_bytes)
        # send file size
        client_socket.send(struct.pack("Q", file_size))
        # send file data in chunks
        sent = 0
        with open(filepath, "rb") as f:
            while sent < file_size:
                chunk = f.read(4096)
                if not chunk:
                    break
                client_socket.sendall(chunk)
                sent += len(chunk)
                # progress indicator
                progress = 100 * (sent / file_size)
                print(f"Progress: {progress:.1f}%", end="\r")
        print("File sent successfully")

        # wait for confirmation from server that it was received
        response = client_socket.recv(1024).decode()
        print(response)
        
    except Exception as e:
        print(f"Error sending file: {e}")

# function to receive file from client
def receive_file(conn):
    try:
        # receive filename length, name, and size
        filename_size = struct.unpack("I", conn.recv(4))[0]
        filename = conn.recv(filename_size).decode()
        file_size = struct.unpack("Q", conn.recv(8))[0]
        print(f"Receiving file: {filename} ({file_size/1e6}Mb)")

        # receive file data in chunks
        received = 0
        with open(f"uploads/{filename}", "wb") as f:
            while received < file_size:
                chunk_size = min(4096, file_size - received)
                chunk = conn.recv(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
                
                # progress indicator
                progress = 100 * (received / file_size)
                print(f"Progress: {progress:.1f}%", end="\r")
        print(f"\nFile received: {filename}")
        conn.sendall(b"File received successfully")
        
    except Exception as e:
        print(f"Error receiving file: {e}")
        conn.sendall(f"Error: {e}".encode())
