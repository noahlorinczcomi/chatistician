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
    return "".join([today, id])

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
