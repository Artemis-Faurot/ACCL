#! /bin/bash

python3 main.py $1
nasm -felf64 output/out.asm -o output/out.o
gcc -static -nostdlib -m64 output/out.o -o output/out
echo "Running program . . ."
echo " "
./output/out
exit_code=$?
echo " "
echo "Program exited with code:" $exit_code