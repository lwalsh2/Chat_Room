# Define / Create libraries
add_library(socket_lib STATIC socket.c)
add_library(client_lib STATIC client_connect.c)
add_library(server_lib STATIC server_bind.c)

# Add Socket compilation flags / links
target_include_directories(socket_lib PUBLIC include)
target_compile_options(socket_lib PUBLIC -Wall)
set(TARGET socket_lib PROPERTY C_STANDARD 11)
set(TARGET socket_lib PROPERTY C_STANDARD_REQUIRED ON)

# Link libraries
target_link_libraries(client_lib PUBLIC socket_lib)
target_link_libraries(server_lib PUBLIC socket_lib)
target_link_libraries(server_lib PRIVATE Threads::Threads)