import socket
import threading
import yaml
import utils
import client_functions
import headers

headers.masthead()

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

# receive name prompt from server.py and enter name
name_prompt = client.recv(1024).decode()
print(name_prompt, end="")
name = input()
client.sendall(name.encode())
headers.welcome(name)

# defining breaking criteria
breakers = config['breakers']['values']
# choosing terminal colors
scolor = utils.colors(config['colors']['server'])
ccolor = utils.colors(config['colors']['client'])
colored_client_name = f"{ccolor[0]}[{name}]{ccolor[1]}"
colored_server_name = f"{scolor[0]}[Chatistician]{scolor[1]}"

# start receiving and sending threads
receive_thread = threading.Thread(
    target=client_functions.receive_messages,
    args=(client, colored_server_name, colored_client_name, breakers)
)
send_thread = threading.Thread(
    target=client_functions.send_messages,
    args=(client, colored_client_name, breakers)
)

receive_thread.start()
send_thread.start()

# wait for both to finish before closing connection
send_thread.join()
receive_thread.join()

# will close once we break out of the loop
client.close()
print("Connection closed")
