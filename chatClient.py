# Client half of the code, meant to connect and communicate with server
# importing socket library to utilize sockets for communication
import socket # Utilize sockets for connections
import errno  # Error handling
import sys	# Alllow for breaks
from datetime import datetime # Timestamps for messages (haven't made Zulu yet)
from cryptography.fernet import Fernet # Encryption

# Grab key for encryption
def read_key():
	try:
		# Open the file the Server made with thee key
		file = open('Definitely_Not_the_Key', 'rb')
		print("Successfully retreived key")
		return file.read()
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

# Connect to the server
def connect(saddr):
	try:
		# Initializing socket:
		# AF_INET refers to Internet Address Family, allowing for outside connections
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Reaching out to the server for a connection
		server_socket.connect(saddr)
		print("Successfully Connected!")
		# Allows for recv to work unhindered
		server_socket.setblocking(False)
		return server_socket
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

# Create and send username to server
def username(server_socket):
	try:
		# Create a name for yourself within the server
		username = input("Username: ")
		# Encode username for server to read
		encoded_username = username.encode('utf-8')
		# Header protocol
		username_length = f"{len(encoded_username):<{10}}".encode('utf-8')
		# Sending username to server to track (0 for add user, 1 for send message)
		server_socket.send(username_length + encoded_username)
		# print(f"Protocol Sent: {username_length + encoded_username}")
		return username
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

# Proceed to chat with server
def chat(server_socket, name, key):
	# Initial Message in chat
	print("You are in the chat server. Use !quit to exit, enter to send/refresh messages")
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
				# Adding timestamp for recordkeeping
				message = str(datetime.now()).split('.')[0] + " : " + message
				# Encode for transport
				message = message.encode('utf-8')
				# Encrypt for security
				message = Fernet(key).encrypt(message)
				message_length = f"{len(message) :< {10}}".encode('utf-8')
				server_socket.send(message_length + message)
				# print(f"Protocol Sent: {message_length + message}")
			# Receiving Messages (expected IOerrors)
			try:
				while True:
					# Receive messages
					junk = server_socket.recv(1)
					username_length = server_socket.recv(10)
					if not len(username_length):
						print("Connection closed by server")
						sys.exit()
					message_length = int(server_socket.recv(10).decode('utf-8').strip())
					username = server_socket.recv(int(username_length.decode('utf-8').strip())).decode('utf-8')
					# Decode to readable string
					message = Fernet(key).decrypt(server_socket.recv(message_length)).decode('utf-8')
					print(f"{username} > {message}")
			except IOError as e:
				if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
					print('Reading error', str(e))
					sys.exit()
				continue
	except Exception as error_message:
		print('General error', str(error_message))
		sys.exit()

def main():
	# Ask for user input for server information, then try to connect
	server_socket = connect((input("Server IP: "), int(input("Server Port: "))))
	name = username(server_socket)
	chat(server_socket, name, read_key())


if __name__ == "__main__":
	main()
