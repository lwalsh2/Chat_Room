/* TCP Chat Client
 * Client half of the code, meant to connect and communicate with server.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

// Message buffer size
#define BUFFER_SIZE 128


// Socket builder method
size_t create_struct(int port, struct sockaddr_in *struct_ptr){
	(*struct_ptr).sin_family = AF_INET; // IPv4
	(*struct_ptr).sin_addr.s_addr = INADDR_ANY; // shortcut for self
	(*struct_ptr).sin_port = htons( port );
	return sizeof(*struct_ptr);
}

// Facilitates the communication between client and server.
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

        // and send that buffer to client
        send(server_socket, message, BUFFER_SIZE, 0);

		// Receive
		if (recv(server_socket, message, sizeof(message), 0) < 0)
		{
			printf("Failed to receive\n");
			break;
		}

        // print buffer which contains the server contents
        printf("<user> %s", message);
    }
}

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

	// Connect to the server
	if (connect(server_socket, (struct sockaddr *)&server_struct, sizeof(server_struct)) < 0)
	{
		printf("Failed to connect\n");
		exit(-1);
	}
	chat_system(server_socket);
}

int main(int argc, char ** argv)
{
    if (argc != 2)
    {
        printf("Client requires one argument - the given port to run on.\n");
        return -1;
    }

    int port = atoi(argv[1]);

    if (port < 80 && port > 4000)
    {
        printf("Invalid Port number.\n");
        return -1;
    }

    // Socket Creation
    run_client(port);
	return 0;
}
