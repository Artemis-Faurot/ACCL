#! /bin/bash
sudo rm -rf /usr/bin/accl/
sudo rm /usr/bin/baccl
sudo mkdir /usr/bin/accl
sudo cp -r ./src /usr/bin/accl/src
sudo cp ./build/build.sh /usr/bin/baccl