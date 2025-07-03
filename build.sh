#!/bin/bash
rm -rf bin
mkdir bin
cmake -B bin -S c_implementation
cd bin
make
