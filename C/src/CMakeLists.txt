# Set thread requirements for Ubuntu 20.04
# (Automatically included in 22.04)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

# Define / Create Executable binaries
add_executable(client cClient.c)
add_executable(server cServer.c)

# Add Client compilation flags / links
target_include_directories(client PRIVATE include)
target_compile_options(client PRIVATE -Wall)
set(TARGET client PROPERTY C_STANDARD 11)
set(TARGET client PROPERTY C_STANDARD_REQUIRED ON)

# Add Server compilation flags / links
target_include_directories(server PRIVATE include)
target_compile_options(server PRIVATE -Wall)
set(TARGET server PROPERTY C_STANDARD 11)
set(TARGET server PROPERTY C_STANDARD_REQUIRED ON)

target_link_libraries(server PRIVATE Threads::Threads)