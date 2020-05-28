# Server half of the code, meant to connect and communicate with clients
# importing socket library to utilize sockets for communication
import socket
import select

HL = 10
sname = "127.0.0.1" # Change to your IP
sport = 1234		# Edit to be the port of your choosing
saddr = (sname, sport)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allow for reuse/reconnect of port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(saddr)
s.listen()
socklist = [s]
clients = {}
def receive_message(client_socket):
	try:
		message_header = client_socket.recv(HL)
		if not len(message_header):
			return False
		message_length = int(message_header.decode("utf-8").strip())
		return{"header": message_header, "data": client_socket.recv(message_length)}
	# Broken script
	except:
		return False


while True:
	read_sockets, _, exception_sockets = select.select(socklist, [], socklist)
	for notified_socket in read_sockets:
		if notified_socket == s:
			client_socket, client_address = s.accept()
			user = receive_message(client_socket)
			if user is False:
				continue
			socklist.append(client_socket)
			clients[client_socket] = user
			print(f"Accepted connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
		else:
			message = receive_message(notified_socket)
			if message is False:
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				socklist.remove(notified_socket)
				del clients[notified_socket]
				continue
			user = clients[notified_socket]
			print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

			for client_socket in clients:
				if client_socket != notified_socket:
					client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

	for notified_socket in exception_sockets:
		socklist.remove(notified_socket)
		del clients[notified_socket]

'''
# Server half of the code, meant to connect and communicate with clients
# importing socket library to utilize sockets for communication
import socket
sname = socket.gethostname() # socket.gethostname("") for MAC
sport = 1234
saddr = (sname, sport)

# s is defined as our server socket for communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET, or Internet Address Family, allows for communication with IPv4 over the internet
# SOCK_STREAM allows for TCP protocols

# Bind lets us attach s to a port. Gethostname lists ourselves for the bind
s.bind(saddr)

# listen defines our connection limit
s.listen(5)

# Let's us continue until the program is halted (Not needed in our case, but as an example)
while 1:
	# Accept incoming connections to our port
	clientsocket, address = s.accept()
	# List who has connected as a client. 'f' let's us call variables
	print(f"Client {address} has entered {sname}'s chat server")
	# Send a message to the client
	clientsocket.send(bytes(f"Welcome to {sname}'s server, {address[0]}", "utf-8"))
	# Disconnect the client from the server
	clientsocket.close()
	# Turn off the Server (Create other conditions for actual server)
	break

# Safe shutdown for the socket
#try:
#	s.shutdown(socket.SHUT_RDWR)
#finally:
s.close()
'''
