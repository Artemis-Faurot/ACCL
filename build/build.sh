#! /bin/bash

cmake -S . -B build/
cmake --build build/
cd ./build
./accl ../$1
nasm -felf64 out.asm -o out.o
gcc -static -nostdlib -m64 out.o -o out
echo "Building complete!"
echo "Running program..."
echo " "
./out
exit_code=$?
echo " "
echo "Program exited with code:" $exit_code