/* Socket Header File
 * Defines buffer size and function
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
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
