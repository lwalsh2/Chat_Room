#!/bin/bash
rm -rf bin client server
mkdir bin
cmake -B bin -S c_implementation
cd bin
make
cd ..
cp bin/src/client .
cp bin/src/server .
