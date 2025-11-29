import socket
import threading
import argparse
from shared import utils as shared_utils
from shared import banners as shared_banners
from client import utils as client_utils
from client import functions as client_functions

def main():
    # local or remote
    parser = argparse.ArgumentParser(
        description="Chat"
    )
    parser.add_argument(
        "--config",
        default="shared/config_local.yaml",
        help="Config .yaml file to use in chat (default is config_local.yaml)"
    )
    args = parser.parse_args()

    # socket config
    config = shared_utils.load_config(args.config)

    HOST = config['client']['host'] # server IP
    PORT = config['client']['port'] # port server is listening on

    # Create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect socket to HOST:PORT
    client.connect((HOST, PORT))
    name = client_utils.assign_client_id()
    client.sendall(name.encode())

    shared_utils.init_footer_config()
    client_utils.print_welcome(name)
    shared_banners.banner()
    # log_file, log_filename = client_utils.open_log(name, config) # start log file

    # defining breaking criteria
    breakers = config['specials']['breakers']
    # choosing terminal colors
    scolor = shared_utils.colors(config['colors']['server'])
    ccolor = shared_utils.colors(config['colors']['client'])
    colored_client_name = f"{ccolor[0]}[{name}]{ccolor[1]}"
    colored_server_name = f"{scolor[0]}[Chatistician]{scolor[1]}"

    # start receiving and sending threads
    receive_thread = threading.Thread(
        target=client_functions.receive_msg,
        args=(client, colored_server_name, colored_client_name, breakers)
    )
    send_thread = threading.Thread(
        target=client_functions.send_msg,
        args=(client, colored_client_name, breakers, args.config)
    )

    receive_thread.start()
    send_thread.start()

    # wait for both to finish before closing connection
    send_thread.join()
    receive_thread.join()

    # will close once we break out of the loop
    # client_utils.close_log(log_file, log_filename)
    shared_utils.close_footer_config()
    client.close()
    print("Connection closed")
    
    return

if __name__ == "__main__":
    main()