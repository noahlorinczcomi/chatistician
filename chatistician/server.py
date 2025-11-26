import socket
import threading
import yaml
import utils
import server_functions
import subprocess
import argparse

def main():
    # local or remote
    parser = argparse.ArgumentParser(
        description="Chat"
    )
    parser.add_argument(
        "--config",
        default="config_local.yaml",
        help="Config .yaml file to use in chat (default is config_local.yaml)"
    )
    args = parser.parse_args()

    subprocess.run('clear', text=True, shell=True)

    # socket config
    config_path = utils.resource_path(args.config)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # socket config
    HOST = config['server']['host'] # server IP
    PORT = config['server']['port'] # port server is listening on

    # Create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # let us reuse the port immediately
    server.listen(int(config['settings']['max_connections']))

    # connect server socket to HOST:PORT and receive client ID
    print("Waiting for client")
    conn, addr = server.accept()
    client_name = conn.recv(1024).decode()
    print(f"{client_name} connected")
    print("Type \"!help\" anytime to privately view full functionality")

    # defining breaking criteria
    breakers = config['breakers']['values']
    # choosing terminal colors
    scolor = utils.colors(config['colors']['server'])
    ccolor = utils.colors(config['colors']['client'])
    colored_client_name = f"{ccolor[0]}[{client_name}]{ccolor[1]}"
    colored_server_name = f"{scolor[0]}[Chatistician]{scolor[1]}"

    # start receiving and sending threads
    receive_thread = threading.Thread(
        target=server_functions.receive_msg,
        args=(conn, colored_client_name, colored_server_name, breakers)
    )
    send_thread = threading.Thread(
        target=server_functions.send_msg,
        args=(conn, colored_server_name, breakers)
    )

    receive_thread.start()
    send_thread.start()

    # above code blocks. Wait for threads to finish before closing conn
    send_thread.join()
    receive_thread.join()

    # close server entirely
    conn.close()
    server.close()
    print("Connection closed")

    return

if __name__ == "__main__":
    main()