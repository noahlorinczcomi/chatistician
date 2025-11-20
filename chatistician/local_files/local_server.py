# Bytes vs Strings: Sockets send/receive bytes (b"..."), so we use .decode() to convert to strings
# Blocking calls: accept(), recv(), and connect() pause execution until they complete
# Two sockets on server: One listens for connections (server), one handles each client (conn)
# Order matters: Server must be running and listening before client tries to connect

import socket
import threading
import yaml
import utils

# socket config
with open('local_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# socket config
HOST = config['server']['host'] # server IP
PORT = config['server']['port'] # port server is listening on

# Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # let us reuse the port immediately
server.listen(int(config['settings']['max_connections']))
print(f"Server listening on {HOST}:{PORT}")

# connect server socket to HOST:PORT
conn, addr = server.accept()
print(f"Connected by {addr}")

# ask for name and receive response
conn.sendall(b"Name: ")
client_name = conn.recv(1024).decode()
print(f"{client_name} has joined the chat")

# defining breaking criteria
breakers = config['breakers']['values']
# choosing terminal colors
scolor = utils.colors(config['colors']['server'])
ccolor = utils.colors(config['colors']['client'])
colored_client_name = f"{ccolor[0]}[{client_name}]{ccolor[1]}"
colored_server_name = f"{scolor[0]}[Chatistician]{scolor[1]}"

def receive_msg():
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"\n{client_name} disconnected")
                break # out of while loop
            msg = data.decode()
            # flush line before receiving, then re-prompt
            # \r\033[K flushes
            print(f"\r\033[K{colored_client_name} {msg}")
            print(f"{colored_server_name} ", end="", flush=True) # re-prompt
            if msg.lower() in breakers:
                conn.close()
                break
        except:
            break

def send_msg():
    while True:
        try:
            msg = input(f"{colored_server_name} ")
            conn.sendall(msg.encode())
            if msg.lower() in breakers:
                conn.close()
                break
        except:
            break

# start receiving and sending threads
receive_thread = threading.Thread(target=receive_msg)
send_thread = threading.Thread(target=send_msg)

receive_thread.start()
send_thread.start()

# above code blocks. Wait for threads to finish before closing conn
send_thread.join()
receive_thread.join()

# close server entirely
conn.close()
server.close()
print("Connection closed")
