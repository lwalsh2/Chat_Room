#!/bin/bash
rm -rf bin build client server Definitely_Not_the_Key
mkdir bin build
cmake -B build -S c_implementation
cd build
make
cd ..
cp build/src/client bin/
cp build/src/server bin/
