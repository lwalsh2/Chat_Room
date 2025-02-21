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
#include "client.h"
#include "socket.h"

/* @brief: Facilitates the communication between client and server.
 * @param: int server_socket - Socket to read and write to
 * @returns: NULL
 */
void chat_system(int server_socket)
{
    int message_index = 0;
    char message[BUFFER_SIZE] = "";

    // Looping Messages/Messaging
    while (1)
    {
        // Read user's message
        printf("\n> ");
        message_index = -1;
        while (message_index < BUFFER_SIZE-1 && (message[++message_index] = getchar()) != '\n' && message[message_index] != '\0');
        message[message_index] = '\n';

        // Send the message to server if there was anything entered.
        if (message_index > 0)
        {
            send(server_socket, message, BUFFER_SIZE, 0);
        }

        // Receive a message from the client.
        if (recv(server_socket, message, sizeof(message), 0) < 0)
        {
            printf("Failed to receive\n");
            break;
        }

        // Print server message
        printf("<user> %s", message);
        sleep(1);
    }
}

/* @brief: Sets up the socket, and tries to connect to the server.
 * @param: int port - Port to connect on
 * @returns: NULL
 */
void run_client(int port)
{
    // IPv4 (AF_INET), TCP (SOCK_STREAM),  Internet Protocol, TCP->0->default
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0)
    {
        printf("Failed to create socket\n");
        return;
    }
    // Create socket address struct
    struct sockaddr_in server_struct;
    struct sockaddr_in *struct_ptr = &server_struct;
    size_t struct_length = create_struct(port, struct_ptr);

    // Connect to the server (replaced sizeof(server_struct) with struct_length)
    if (connect(server_socket, (struct sockaddr *)struct_ptr, struct_length) < 0)
    {
        printf("Failed to connect\n");
        return;
    }
    chat_system(server_socket);
}
