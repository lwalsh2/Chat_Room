# Server half of the code, meant to connect and communicate with clients
# importing socket library to utilize sockets for communication
# Host to network (HTON, Network to Host)
# Wire Protocol
# C: thread that accepts, thread per client
# Exit, how to shut down (Next thrusday 1600)
import socket # Utilize sockets for connections
import select # Specifically select.select()
from cryptography.fernet import Fernet # Encryption

# Header length/size
HL = 10

# Create and write a key for encryption
def create_key():
    key = Fernet.generate_key()
    print(f"Your current key is: {key}")
    file = open('Definitely_Not_the_Key', 'wb')
    file.write(key)
    file.close()
    return key

# Bind, Listen, Accept, Begin -- Change s name, and try except
def connect(saddr):
    # Initializing socket:
    # AF_INET refers to Internet Address Family, allowing for outside connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow for reuse/reconnect of port
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(saddr)
    server_socket.listen()
    print("Successfully bound IP and Port")
    return server_socket

def client_left(exception_sockets, socklist, clients):
	# Remove exiting sockets
	for notified_socket in exception_sockets:
		socklist.remove(notified_socket)
		del clients[notified_socket]
	return exception_sockets, socklist, clients

# Receive client input
def receive_message(client_socket):
	try:
		message_header = client_socket.recv(HL)
		if not len(message_header):
			return False
		message_length = int(message_header.decode('utf-8').strip())
		return{"header": message_header, "data": client_socket.recv(message_length)}
	# Broken script
	except:
		return False

# Accept and comminicate with clients -- No signle-nomatic variables
def run_server(server_socket, key):
	# initialize client socket lists
	socklist = [server_socket]
	clients = {}
	while True:
		# Accept/Post read sockets, and delete exception sockets (incoming and leaving)
		read_sockets, _, exception_sockets = select.select(socklist, [], socklist)
		# Go through sockets
		for notified_socket in read_sockets:
			# Socket is incoming client
			if notified_socket == server_socket:
				client_socket, client_address = server_socket.accept()
				# Receive the username
				user = receive_message(client_socket)
				# If no name, or error, skip
				if user is False:
					continue
				# Add user to the lists of clients
				socklist.append(client_socket)
				clients[client_socket] = user
				print(f"Accepted connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
			# Socket is client posting message
			else:
				message = receive_message(notified_socket)
				if message is False:
					print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
					socklist.remove(notified_socket)
					del clients[notified_socket]
					continue
				user = clients[notified_socket]
				print(f"Received message from {user['data'].decode('utf-8')}: {Fernet(key).decrypt(message['data']).decode('utf-8')}")
				# Post message to other clients
				for client_socket in clients:
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
		# Remove exiting clients
		exception_sockets, socklist, clients = client_left(exception_sockets, socklist, clients)

def main():
    # Ask for user input for server information, then try to connect
	server_socket = connect((input("Server IP: "), int(input("Server Port: "))))
	run_server(server_socket, create_key())

if __name__ == "__main__":
    main()
