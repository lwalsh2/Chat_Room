# ChatRoom
This is a Chat Room project that utilizes Sockets and encryption in Python. Meant for better understanding concepts of sockets, server/client operations, and encrypting messages.

Client Imports: (Python)
	socket, errno, sys, datetime, cryptography

Server Imports: (Python)
	socket, select, sys, cryptography


Operation: (Python)

	chatServer acts as the chat room server/host for clients/users to connect to. By binding a socket to a user-determined IP and Port, chatServer listens for requests to connect, and for incoming messages. Incoming users are saved, and messages are broadcasted to the other users.

	chatClient acts as the chat room client/user, meant to connect to the server and send/receive messages. chatClient creates a socket to connect to the server's Multiple users connect at a time, and any user who sends a message to the server has the message broadcasted to the other users.

Imports: (C)
	stdio.h, stdlib.h, sys/socket.h, sys/types.h, netinet/in.h

Operation: (C)
	cServer creates a socket, and sends the first client to connect a message before quitting.

	cClient connects to the server, and prints the received message.
