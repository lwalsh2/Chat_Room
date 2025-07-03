# ChatRoom
This is a Chat Room project that utilizes Sockets and encryption in Python. Meant for better understanding concepts of sockets, server/client operations, and encrypting messages.

## Client Imports: (Python)
socket, errno, sys, datetime, cryptography

## Server Imports: (Python)
socket, select, sys, cryptography

## Operation: (Python)
`server.py` acts as the chat room server/host for clients/users to connect to. By binding a socket to a user-determined IP and Port, `server.py` listens for requests to connect, and for incoming messages. Incoming users are saved, and messages are broadcasted to the other users.

`client.py` acts as the chat room client/user, meant to connect to the server and send/receive messages. `client.py` creates a socket to connect to the server's Multiple users connect at a time, and any user who sends a message to the server has the message broadcasted to the other users.

## Imports: (C)
stdio.h, stdlib.h, string.h, sys/socket.h, sys/types.h, netinet/in.h, unistd.h

## Operation: (C)
To build the binaries, you can run the `build.sh` script, or if you have Python's invoke module, you can run `invoke build`. The `client` and `server` binaries are moved to the `bin/`. The binaries can be run with the port they should run on.
```sh
./bin/server 5555
```
```sh
./bin/client 5555
```

Server takes an argument for the port to bind on, and listens for clients. Displays the client and the message the client sends.

Client takes an argument for a port to connect to, and sends messages to the server. Listens for incoming messages.
