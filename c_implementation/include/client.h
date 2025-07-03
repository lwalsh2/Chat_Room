/* Client Header File
 * Defines buffer size and functions
*/

/* @brief: Facilitates the communication between client and server.
 * @param: int server_socket - Socket to read and write to
 * @returns: NULL
 */
void chat_system(int server_socket);

/* @brief: Sets up the socket, and tries to connect to the server.
 * @param: int port - Port to connect on
 * @returns: NULL
 */
void run_client(int port);
