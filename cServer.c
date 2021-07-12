#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>


// Socket builder method
size_t create_struct(int port, struct sockaddr_in *struct_ptr){
	(*struct_ptr).sin_family = AF_INET; // IPv4
	(*struct_ptr).sin_addr.s_addr = INADDR_ANY; // shortcut for self
	(*struct_ptr).sin_port = htons( port );
	return sizeof(*struct_ptr);
}


int main() {
	// Socket Creation
	// IPv4 (AF_INET), TCP (SOCK_STREAM),  Internet Protocol, TCP->0->default
	printf("Creating Socket\n");
	int server_socket = socket(AF_INET, SOCK_STREAM, 0);
	if (server_socket < 0)
	{
		printf("Failed to create socket\n");
		exit(-1);
	}
	// System call that allows for reuse of IP address and port
	printf("Overriding previous bind\n");
	int option_value = 1;
	if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &option_value, sizeof(option_value)) < 0)
	{
		printf("Failed to reuse\n");
		exit(-1);
	}
	// int setsockopt(int socket, int level, int option_name, const void *option_value, socklen_t option_len);

	// Create socket address struct
	printf("Creating Struct\n");
	// Defining socket
	struct sockaddr_in server_struct;
	struct sockaddr_in *struct_ptr = &server_struct;
	size_t struct_length = create_struct(1234, struct_ptr);

	// Bind the socket to IP address and Port
	printf("Binding socket\n");
	if ((bind(server_socket, (struct sockaddr *)&server_struct, struct_length)) < 0)
	{
		printf("Failed to bind\n");
		exit(-1);
	}
	// Turns socket into a listener (listens for connections, and backlogs up to 5)
	printf("Listening for Clients\n");

	// Declare variables for incoming clients
	int client_socket;
	// Listen for incoming clients (backhaul of 5)
	if (listen(server_socket, 5) < 0)
	{
		printf("Failed to accept\n");
		exit(-1);
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

		// Send message to CLient
		char message[256] = "This is the message - Server";
		send(client_socket, message, sizeof(message) , 0);
		// Receive
		if (recv(client_socket, message, sizeof(message), 0) < 0)
		{
			printf("Failed to receive\n");
			break;
		}
		printf("%s", message);
	}
  return 0;
}
