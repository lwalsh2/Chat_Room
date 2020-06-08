# Server half of the code, meant to connect and communicate with clients
# importing socket library to utilize sockets for communication
import socket # Utilize sockets for connections
import select # Specifically select.select()

HL = 10                 # Header length/size
sname = "192.168.0.3"   # Change to your IP
sport = 80		        # Edit to be the port of your choosing
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
	# Accept/Post read sockets, and delete exception sockets (incoming and leaving)
	read_sockets, _, exception_sockets = select.select(socklist, [], socklist)
	# Go through sockets
	for notified_socket in read_sockets:
		# Socket is incoming client
		if notified_socket == s:
			client_socket, client_address = s.accept()
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
			print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
			# Post message to other clients
			for client_socket in clients:
				if client_socket != notified_socket:
					client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
	# Remove exiting sockets
	for notified_socket in exception_sockets:
		socklist.remove(notified_socket)
		del clients[notified_socket]
