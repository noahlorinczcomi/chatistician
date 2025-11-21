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
            print(f"{colored_client_name} ", end="", flush=True)  # Re-prompt
            if msg.lower() in breakers:
                client.close()
                break
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
                client.close()
                break
        except Exception as e:
            print(f"Error: {e}")
            break
