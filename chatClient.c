#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

// Socket builder method
struct sockaddr_in create_struct(int port){
	struct sockaddr_in server_struct;
	server_struct.sin_family = AF_INET; // IPv4
	server_struct.sin_addr.s_addr = INADDR_ANY; // shortcut for self
	server_struct.sin_port = htons( port );
	return server_struct;
}


int main() {
	// Socket Creation
	// IPv4 (AF_INET), TCP (SOCK_STREAM),  Internet Protocol, TCP->0->default
	int client_socket = socket(AF_INET, SOCK_STREAM, 0);

	// Create socket address struct
	struct sockaddr_in server_struct = create_struct(1234);

	// Connect to the server
	connect(client_socket, (struct sockaddr *)&server_struct, sizeof(server_struct));

	// Receive from server
	char message[256] = "";
	int wasRecv = recv(client_socket, message, sizeof(message), 0);
	printf("%s", message);

	printf("\nFinished\n");

	return 0;
}
