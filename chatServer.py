# Client half of the code, meant to connect and communicate with server
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
