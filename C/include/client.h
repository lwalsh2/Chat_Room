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
void chat_system(int server_socket);

// Sets up the socket, and tries to connect to the server.
void run_client(int port);
