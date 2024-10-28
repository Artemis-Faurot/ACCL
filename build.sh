#! /bin/bash
debug=0
rm -rf ./output
mkdir ./output
python3 main.py $1
py_exit_code=$?
if [ $py_exit_code -eq 0 ]; then
  nasm -felf64 output/out.asm -o output/out.o
  gcc -static -nostdlib -m64 output/out.o -o output/out
  echo "Running program . . ."
  echo " "
  ./output/out
  accl_exit_code=$?
  echo " "
  echo "Program exited with code:" $accl_exit_code
fi
if [ $debug -eq 0 ]; then
  rm -rf ./output
fi