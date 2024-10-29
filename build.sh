#! /bin/bash
debug=0
rm -rf ./output
mkdir ./output
filename=$(basename $1 .accl)
python3 /usr/bin/accl_src/main.py $1
py_exit_code=$?
if [ $py_exit_code -eq 0 ]; then
  nasm -felf64 output/out.asm -o output/out.o
  gcc -static -nostdlib -m64 output/out.o -o "$filename"
  echo "Running program . . ."
  echo " "
  ./$filename
  accl_exit_code=$?
  echo " "
  echo "Program exited with code:" $accl_exit_code
fi
if [ $debug -eq 0 ]; then
  rm -rf ./output
fi