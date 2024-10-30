#! /bin/bash
sudo rm -rf /usr/bin/accl/src
sudo cp -r ./src /usr/bin/accl/src
sudo cp ./build/run.sh /usr/bin/accl/run
sudo cp ./build/build.sh /usr/bin/baccl