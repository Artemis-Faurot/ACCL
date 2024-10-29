#! /bin/bash
filename=$(basename $1 .accl)
echo "Running program . . ."
echo " "
./$filename
accl_exit_code=$?
echo " "
echo "Program exited with code:" $accl_exit_code