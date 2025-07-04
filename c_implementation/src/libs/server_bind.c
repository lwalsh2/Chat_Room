/* Client Header File
 * Defines buffer size and functions
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include "server.h"
#include "socket.h"

void chat_system(int client_socket)
{
    char message[BUFFER_SIZE] = "";

    // Looping Messages/Messaging
    while (1)
    {
        // Receive a message from the client.
        if (recv(client_socket, message, sizeof(message), 0) < 0)
        {
            printf("Failed to receive\n");
            break;
        }
        // Print the Client's message
        printf("<user> %s", message);

        // Send the message to client. TODO: convert to a broadcast to other clients
        send(client_socket, message, BUFFER_SIZE, 0);
    }
}

void start_server(int port)
{
    // IPv4 (AF_INET), TCP (SOCK_STREAM),  Internet Protocol, TCP->0->default
    printf("Creating Socket\n");
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0)
    {
        printf("Failed to create socket\n");
        return;
    }
    // System call that allows for reuse of IP address and port
    printf("Set socket to override\n");
    int option_value = 1;
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &option_value, sizeof(option_value)) < 0)
    {
        printf("Failed to reuse\n");
        return;
    }
    // int setsockopt(int socket, int level, int option_name, const void *option_value, socklen_t option_len);

    // Create socket address struct
    printf("Creating Struct\n");
    // Defining socket
    struct sockaddr_in server_struct;
    struct sockaddr_in *struct_ptr = &server_struct;
    size_t struct_length = create_struct(port, struct_ptr);

    // Bind the socket to IP address and Port
    printf("Binding socket\n");
    if ((bind(server_socket, (struct sockaddr *)&server_struct, struct_length)) < 0)
    {
        printf("Failed to bind\n");
        return;
    }

    // Turns socket into a listener (listens for connections, and backlogs up to 5)
    printf("Listening for Clients\n");

    // Declare variables for incoming clients
    int client_socket;
    // Listen for incoming clients (backhaul of 5)
    if (listen(server_socket, 5) < 0)
    {
        printf("Listen failed.\n");
        return;
    }
    // Loop Listen-Accept-Send commands. Can be CTRL-C'd out
    while(1) {
        // Accept incoming client (Was the cause of earlier issue)
        if ((client_socket = accept(server_socket, (struct sockaddr *)&server_struct, (socklen_t*)&struct_length))<0)
        {
            printf("Failed to accept\n");
            break;
        }
        printf("Received a client: %d\n", client_socket);

        chat_system(client_socket);
    }

    // After chatting close the socket(s)
    close(client_socket);
    close(server_socket);
}
