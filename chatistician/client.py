import socket
import threading
import yaml
import utils
import client_functions
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

    utils.banner()

    # socket config
    config_path = utils.resource_path(args.config)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    HOST = config['client']['host'] # server IP
    PORT = config['client']['port'] # port server is listening on

    # Create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect socket to HOST:PORT
    client.connect((HOST, PORT))
    name = client_functions.assign_client_id()
    client.sendall(name.encode())
    utils.welcome(name)

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

    return

if __name__ == "__main__":
    main()