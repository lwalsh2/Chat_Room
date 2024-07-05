#!/bin/bash

rm -r bin
mkdir -p bin
cd bin
cmake ..
make -j$(nproc)
cd ..
