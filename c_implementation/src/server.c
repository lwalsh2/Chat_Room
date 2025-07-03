/* TCP Chat Server
 * By: Liam P. Walsh
 * Server half of the code, meant to connect and communicate with clients.
 * Currently echoes message from 1 client.
 * Host to network
*/
#include <stdio.h>
#include "server.h"
#include "socket.h"

// @brief: Main function that sets up and runs the client calls
int main(int argc, char ** argv)
{
    // Verify the argument count is 2 (Check if the user specified a port)
    if (argc != 2)
    {
        printf("Server requires one argument - the given port to run on.\n");
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
    start_server(port);

    return 0;
}
