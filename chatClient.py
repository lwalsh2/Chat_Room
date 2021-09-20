"""
Client half of the code, meant to connect and communicate with server
importing socket library to utilize sockets for communication
"""
# Utilize sockets for connections
import socket
# Error handling
import errno
# Allows for breaks
import sys
# Timestamps for messages
from datetime import datetime
# Encryption
from cryptography.fernet import Fernet


def read_key():
    """
    Grabs key for encryption

    Returns
    -------
    file.read(): String
        String contents of the key-file.
    """
    try:
        # Open the file the Server made with thee key
        file = open('Definitely_Not_the_Key', 'rb')
        print("Successfully retrieved key")
        return file.read()
    except Exception as error_message:
        print('General error', str(error_message))
        sys.exit()


def connect(s_address):
    """
    Connects to the server

    Parameter
    ---------
    s_address:

    Returns
    -------
    client_socket:
    """
    try:
        # Initializing socket:
        # AF_INET refers to Internet Address Family,
        # allowing for outside connections
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Reaching out to the server for a connection
        client_socket.connect(s_address)
        print("Successfully Connected!")
        # Allows for receive to work unhindered
        client_socket.setblocking(False)
        return client_socket
    except Exception as error_message:
        print('General error', str(error_message))
        sys.exit()


def username(client_socket, name):
    """
    Creates and send username to server

    Parameters
    ----------
    client_socket:
    name:

    Returns
    -------
    name:
    """
    try:
        # Encode username for server to read
        encoded_name = name.encode('utf-8')
        # Header protocol
        name_length = len(encoded_name).to_bytes(4, 'big')
        # Sending username to server to track (0 for add user,
        # 1 for send message)
        client_socket.send(name_length + encoded_name)
        # print(f"Protocol Sent: {username_length + encoded_username}")
        return name
    except Exception as error_message:
        print('General error', str(error_message))
        sys.exit()


def chat(client_socket, name, key):
    """
    Proceed to chat with server

    Parameters
    ----------
    client_socket:
    name:
    key:
    """
    # Initial Message in chat
    print("You are in the chat server. Use !quit to",
          "exit, enter to send/refresh messages")
    # Looping Messages/Messaging
    try:
        while True:
            # Enter message to send to chat (enter to refresh chat log)
            message = input(f"{name} > ")
            # Provide a quit function
            if message == "!quit":
                print("Leaving Chat. Goodbye!")
                sys.exit()
            # Returns true if a message was typed. Otherwise refreshes
            if message:
                # Adding timestamp for record keeping
                message = str(datetime.now()).split('.')[0] + " : " + message
                # Encode for transport
                message = message.encode('utf-8')
                # Encrypt for security
                message = Fernet(key).encrypt(message)
                message_length = len(message).to_bytes(4, 'big')
                client_socket.send(message_length + message)
            # Receiving Messages (expected IO errors)
            try:
                while True:
                    # Receive messages
                    username_length = client_socket.recv(4)
                    if not len(username_length):
                        print("Connection closed by server")
                        sys.exit()
                    message_length = int.from_bytes(client_socket.recv(4),
                                                    'big')
                    user = client_socket.recv(int.from_bytes(
                        username_length, 'big')).decode('utf-8')
                    # Decode to readable string
                    message = Fernet(key).decrypt(
                        client_socket.recv(message_length)).decode('utf-8')
                    print(f"{user} > {message}")
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error', str(e))
                    sys.exit()
                continue
    except Exception as error_message:
        print('General error', str(error_message))
        sys.exit()


def main():
    """
    Accepts Parameters of IP, Port and Username
    (i.e. py chatClient 192.168.0.1 80 Bob)
    """
    if len(sys.argv) > 3:
        client_socket = connect((sys.argv[1], int(sys.argv[2])))
        name = username(client_socket, sys.argv[3])
    elif len(sys.argv) > 2:
        client_socket = connect((sys.argv[1], int(sys.argv[2])))
        name = username(client_socket, input("Username: "))
    elif len(sys.argv) > 1:
        client_socket = connect((sys.argv[1], int(input("Server Port: "))))
        name = username(client_socket, input("Username: "))
    else:
        # Ask for user input for server information, then try to connect
        client_socket = connect((input("Server IP: "),
                                 int(input("Server Port: "))))
        name = username(client_socket, input("Username: "))
    chat(client_socket, name, read_key())


if __name__ == "__main__":
    main()
