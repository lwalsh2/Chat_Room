# Client half of the code, meant to connect and communicate with server
# importing socket library to utilize sockets for communication
import socket

# s is defined as our client socket for communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET refers to the IPv4, and SOCK_STREAM allows for ___
s.connect((socket.gethostname(), 1234))

# Create a var to print off small or large messages
chatmsg = ''
# Loop ensures the message isn't capped off from size
while True:
    # Receive message from server: Number represents buffer's byte-size
    msg = s.recv(8)
    # If the message is finished, break
    if len(msg) <= 0:
        break
    # Convert and print server's greeting, adding it to the main message
    chatmsg += msg.decode("utf-8")
# Print off the full message from the server
print(chatmsg)
