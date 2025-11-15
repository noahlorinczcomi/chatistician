import socket
import threading
import yaml
import utils

# socket config
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

HOST = config['server']['host'] # server IP
PORT = config['server']['port'] # port server is listening on

# Create client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect socket to HOST:PORT
client.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

# receive name prompt from server.py and enter name
name_prompt = client.recv(1024).decode()
print(name_prompt, end="")
name = input()
client.sendall(name.encode())

# defining breaking criteria
breakers = config['breakers']['values']
# choosing terminal colors
scolor = utils.colors(config['colors']['server'])
ccolor = utils.colors(config['colors']['client'])
colored_client_name = f"{ccolor[0]}[{name}]{ccolor[1]}"
colored_server_name = f"{scolor[0]}[Chatistician]{scolor[1]}"

def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("\nServer disconnected")
                break
            msg = data.decode()
            # flush line before receiving, then re-prompt
            # \r\033[K flushes
            print(f"\r\033[K{colored_server_name} {msg}")
            print(f"{colored_client_name} ", end="", flush=True)  # Re-prompt
            if msg.lower() in breakers:
                client.close()
                break
        except:
            break

def send_messages():
    while True:
        try:
            msg = input(f"{colored_client_name} ")
            client.sendall(msg.encode())
            if msg.lower() in breakers:
                client.close()
                break
        except:
            break

# start receiving and sending threads
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()

# wait for both to finish before closing connection
send_thread.join()
receive_thread.join()

# will close once we break out of the loop
client.close()
print("Connection closed")