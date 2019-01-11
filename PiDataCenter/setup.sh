#! /bin/bash
set -e
set -x
sudo apt-get -y update
sudo apt-get install -y cmake git
sudo apt-get install -y libopenblas-dev libopencv-dev

# required by opencv
sudo apt-get install libhdf5-dev libhdf5-serial-dev
sudo apt-get install libqtwebkit4 libqt4-test

condadir="/home/pi/miniconda3"
if [[ ! -d $condadir ]]; then
    wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
    sudo chmod +x Miniconda3-latest-Linux-armv7l.sh
    ./Miniconda3-latest-Linux-armv7l.sh -b -p /home/pi/miniconda3
fi
var='export PATH="/home/pi/miniconda3/bin:$PATH"'
if ! grep -e miniconda3  ~/.bashrc > /dev/null; then
    echo $var >> ~/.bashrc
fi
PATH="/home/pi/miniconda3/bin:$PATH"
conda create --name py34 python=3.4 -y
source /home/pi/miniconda3/bin/activate py34
pip install --upgrade pip

sudo echo "[global]" > /etc/pip.conf
sudo echo "extra-index-url=https://www.piwheels.hostedpi.com/simple" > /etc/pip.conf
pip install opencv-contrib-python-headless
