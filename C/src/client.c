/* TCP Chat Client
 * By: Liam P. Walsh
 * Client half of the code, meant to connect and communicate with server.
 */
#include <stdio.h>
#include "client.h"
#include "socket.h"

// @brief: Main function that sets up and runs the client calls
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
    if (port < PORT_MIN && port > PORT_MAX)
    {
        printf("Invalid Port number.\n");
        return -1;
    }

    // Socket Creation
    run_client(port);
    return 0;
}
