#!/bin/bash

# Clear out the bin folder if present before building new binaries
rm -rf bin
mkdir -p bin
cd bin
cmake ..
make -j$(nproc)
cp src/client client
cp src/server server
cd ..
