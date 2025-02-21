/* TCP Chat Server
 * Server half of the code, meant to connect and communicate with clients.
 * Currently echoes message from 1 client.
 * Host to network
*/

/* @brief: Function designed for chat between client and server.
 * @param: int client_socket - Socket to read and write to
 * @returns: NULL
 */
void chat_system(int client_socket);

/* @brief: Sets up the socket, and tries to connect to the server.
 * @param: int port - Port to listen on
 * @returns: NULL
 */
void start_server(int port);
