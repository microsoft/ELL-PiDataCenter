#! /bin/bash
set -e
set -x
sudo apt-get -y update
sudo apt-get install -y cmake
sudo apt-get install -y libopenblas-dev
sudo apt-get install -y libopencv-dev

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
conda config --add channels "microsoft-ell"
conda install -y -c microsoft-ell/label/stretch opencv
