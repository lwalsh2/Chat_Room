#!/bin/bash
rm -rf bin build client server
mkdir bin build
cmake -B build -S c_implementation
cd build
make
cd ..
cp build/src/client bin/
cp build/src/server bin/
