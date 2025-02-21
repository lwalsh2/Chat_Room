# Set thread requirements for Ubuntu 20.04
# (Automatically included in 22.04)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

# Define / Create Executable binaries
add_executable(client client.c)
add_executable(server server.c)

add_subdirectory(libs)

# Link libraries
target_link_libraries(client PRIVATE client_lib)
target_link_libraries(server PRIVATE server_lib)
