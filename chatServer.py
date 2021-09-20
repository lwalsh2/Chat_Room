"""
Server half of the code, meant to connect and communicate with clients
importing socket library to utilize sockets for communication
Host to network
Wire Protocol idea for C: thread that accepts, thread per client
Exit, how to shut down
"""
# Utilize sockets for connections
import socket
# Specifically select.select()
import select
# Allow for breaks
import sys
# Encryption
from cryptography.fernet import Fernet


def create_key():
    """
    Creates and write a key for encryption

    Returns
    -------
    key: Encryption Key
    Server-Generated encryption key.
    """
    try:
        key = Fernet.generate_key()
        print(f"Your current key is: {key}")
        file = open('Definitely_Not_the_Key', 'wb')
        file.write(key)
        file.close()
        return key
    except Exception as error_message:
        print('General error', str(error_message))
        sys.exit()


def connect(s_address):
    """
    Bind, Listen, Accept, Begin -- Change s name, and try except
    """
    try:
        # Initializing socket:
        # AF_INET refers to Internet Address Family, (specifically IPv4)
        # allowing for outside connections
        # SOCK_STREAM refers to TCP Connection (DGRAM for UDP)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow for reuse/reconnect of port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(s_address)
        server_socket.listen()
        print("Successfully bound IP and Port")
        return server_socket
    except Exception as error_message:
        print('General error', str(error_message))
        sys.exit()


def client_left(exception_sockets, socket_list, client_names):
    """
    Removes exiting sockets

    Returns
    -------
    exception_sockets:
    socket_list:
    client_names:
    """
    try:
        for notified_socket in exception_sockets:
            socket_list.remove(notified_socket)
            del client_names[notified_socket]
        return exception_sockets, socket_list, client_names
    except Exception as error_message:
        print('General error', str(error_message))
        sys.exit()


def receive_data(client_socket):
    """
    Receives client input
    """
    try:
        message_header = client_socket.recv(4)
        if len(message_header):
            message_length = int.from_bytes(message_header, 'big')
            return{"length": message_header,
                   "data": client_socket.recv(message_length)}
        return False
    except Exception:
        # No user
        return False


def run_server(server_socket, key):
    """
    Accepts and communicates with clients
    """
    try:
        # initialize client socket lists
        socket_list = [server_socket]
        client_names = {}
        while True:
            # Accept/Post read sockets, and delete exception sockets
            # (incoming and leaving)
            # select.select waits for 1 of three events: reads, writes,
            # and exceptions
            # (we use read for incoming connections/messages,
            # and exceptions for lost clients)
            read_sockets, write_sockets, exception_sockets = select.select(
                socket_list, [], socket_list, 1)
            # Go through sockets
            for notified_socket in read_sockets:
                # Socket is incoming client
                if notified_socket == server_socket:
                    client_socket, client_address = server_socket.accept()
                    # Receive the username
                    user = receive_data(client_socket)
                    # If no name, or error, skip
                    if user:
                        # Add user to the lists of clients
                        socket_list.append(client_socket)
                        client_names[client_socket] = user
                        print(f"Accepted connection from {client_address[0]}:",
                              f"{client_address[1]}",
                              f"username: {user['data'].decode('utf-8')}")
                # Socket is client posting message
                else:
                    message = receive_data(notified_socket)
                    if message is False:
                        print(f"Closed connection from ",
                              f"{client_names[notified_socket]['data'].decode('utf-8')}")
                        socket_list.remove(notified_socket)
                        del client_names[notified_socket]
                        continue
                    user = client_names[notified_socket]
                    print(f"Received message from ",
                      f"{user['data'].decode('utf-8')}: ",
                      f"{Fernet(key).decrypt(message['data']).decode('utf-8')}")
                    # Post message to other clients
                    for client_socket in client_names:
                        if client_socket != notified_socket:
                            client_socket.send(user['length'] +
                                               message['length'] +
                                               user['data'] + message['data'])
            # Remove exiting clients
            exception_sockets, socket_list, client_names = \
                client_left(exception_sockets, socket_list, client_names)
    except KeyboardInterrupt:
        print("Goodbye")
        sys.exit()
    except Exception as error_message:
        print('General error', str(error_message))
        sys.exit()


def main():
    """
    Accepts Parameters of IP and Port
    (i.e. py chatServer 192.168.0.1 80)
    """
    if len(sys.argv) > 2:
        server_socket = connect((sys.argv[1], int(sys.argv[2])))
        run_server(server_socket, create_key())
    elif len(sys.argv) > 1:
        server_socket = connect((sys.argv[1], int(input("Server Port: "))))
        run_server(server_socket, create_key())
    else:
        # Ask for user input for server information, then try to connect
        # print("in main")
        server_socket = connect((input("Server IP: "),
                                 int(input("Server Port: "))))
        run_server(server_socket, create_key())


if __name__ == "__main__":
    # print("in _name_")
    print("Welcome to the Chat Server!\nIf you wish to exit at any time,",
          " use CTRL-C.\nFill out following to start:")
    main()
