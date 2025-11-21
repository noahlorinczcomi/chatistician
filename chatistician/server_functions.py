
# receive message
def receive_msg(
    conn,
    colored_client_name,
    colored_server_name,
    breakers
):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print(f"\n{colored_client_name} disconnected")
                break # out of while loop
            msg = data.decode()
            # flush line before receiving, then re-prompt
            # \r\033[K flushes
            print(f"\r\033[K{colored_client_name} {msg}")
            print(f"{colored_server_name} ", end="", flush=True) # re-prompt
            if msg.lower() in breakers:
                conn.close()
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# send message
def send_msg(
    conn,
    colored_server_name,
    breakers
):
    while True:
        try:
            msg = input(f"{colored_server_name} ")
            conn.sendall(msg.encode())
            if msg.lower() in breakers:
                conn.close()
                break
        except:
            break
