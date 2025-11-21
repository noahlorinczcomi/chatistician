import socket
import threading
import yaml
import utils

# socket config
config_path = utils.resource_path('config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

HOST = config['client']['host'] # server IP
PORT = config['client']['port'] # port server is listening on

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

            # if sending a file
            if msg.startswith(":upload"):
                filepath = msg.split(" ", 1)[1].strip()
                if os.path.exists(filepath):
                    send_file(client, filepath)
                else:
                    print(f"File not found: {filepath}")
            elif msg.lower() in breakers:
                client.send(b'T') # send so server knows to expect text
                client.close()
                break
            else:
                client.send(b'T')  # send so server knows to expect text
                client.sendall(msg.encode())
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
