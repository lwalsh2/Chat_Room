# Client half of the code, meant to connect and communicate with server
# importing socket library to utilize sockets for communication
import socket

# s is defined as our client socket for communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET refers to the IPv4, and SOCK_STREAM allows for ___
s.connect((socket.gethostname(), 1234))

# Receive message from server: Number represents buffer's byte-size
msg = s.recv(1024)

# Convert and print server's greeting
print(msg.decode("utf-8"))
