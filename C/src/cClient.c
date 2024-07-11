/* TCP Chat Client
 * By: Liam P. Walsh
 * Client half of the code, meant to connect and communicate with server.
 */
*/
#include "cClient.h"

// Main function that sets up and runs the client calls
int main(int argc, char ** argv)
{
		// Verify the argument count is 2 (Check if the user specified a port)
		if (argc != 2)
    {
        printf("Client requires one argument - the given port to run on.\n");
        return -1;
    }

		// Convert the port argument to an integer.
    int port = atoi(argv[1]);

		// Verify the port range.
    if (port < 80 && port > 4000)
    {
        printf("Invalid Port number.\n");
        return -1;
    }

    // Socket Creation
    run_client(port);
	return 0;
}

/* Facilitates the communication between client and server.
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

/* Sets up the socket, and tries to connect to the server.
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
		exit(-1);
	}
	// Create socket address struct
	struct sockaddr_in server_struct;
	struct sockaddr_in *struct_ptr = &server_struct;
	size_t struct_length = create_struct(1234, struct_ptr);

	// Connect to the server (replaced sizeof(server_struct) with struct_length)
	if (connect(server_socket, (struct sockaddr *)&server_struct, struct_length) < 0)
	{
		printf("Failed to connect\n");
		exit(-1);
	}
	chat_system(server_socket);
}
