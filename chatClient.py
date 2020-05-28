# Client half of the code, meant to connect and communicate with server
# importing socket library to utilize sockets for communication
import socket
import select
import errno
import sys
from datetime import datetime as dt

# Initial variables:
HL = 10             # Header length/size
sname = "127.0.0.1" # Add the Server's IP here
sport = 1234        # Add the server's port here
saddr = (sname, sport) # Makes connect command easier to look at


# Initializing socket:
# AF_INET refers to Internet Address Family, allowing for outside connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Reaching out to the server for a connection
s.connect(saddr)
# Allows for recv to work unhindered
s.setblocking(False)


# Update Username to Server:
# Create a name for yourself within the server
name = input("Username: ")
# Socket information is sent through bytes, so encoding is necessary
uname = name.encode('utf-8')
# Header size for uname
unameH = f"{len(uname):<{HL}}".encode('utf-8')
# Sending username to server to track
s.send(unameH + uname)


# Initial Message in chat
print("You are in the chat server. Use !quit to exit, enter to send/refresh messages")


# Looping Messages/Messaging
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
        message = str(dt.now()).split('.')[0] + " : " + message
        message = message.encode('utf-8')
        messageH = f"{len(message) :< {HL}}".encode('utf-8')
        s.send(messageH + message)
    # Receiving Messages (expected IOerrors)
    try:
        while True:
            # Receive messages
            unameH = s.recv(HL)
            if not len(unameH):
                print("Connection closed by server")
                sys.exit()
            unameL = int(unameH.decode('utf-8').strip())
            uname = s.recv(unameL).decode('utf-8')
            messageH = s.recv(HL)
            messageL = int(messageH.decode('utf-8').strip())
            message = s.recv(messageL).decode('utf-8')
            print(f"{uname} > {message}")
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue
    except Exception as e:
        print('General error', str(e))
        sys.exit()



'''
# Client half of the code, meant to connect and communicate with server
# importing socket library to utilize sockets for communication
import socket
# Size of header
header = 10
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
'''
