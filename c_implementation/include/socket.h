/* Socket Header File
 * Defines buffer size and function
*/
#include <stdlib.h>
#include <netinet/in.h>

// Message buffer size
#define BUFFER_SIZE 2048
#define PORT_MAX __UINT16_MAX__
#define PORT_MIN 1024

// Socket builder method
size_t create_struct(int port, struct sockaddr_in *struct_ptr);
