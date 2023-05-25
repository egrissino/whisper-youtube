#!/bin/bash
sudo yum update
sudo yum install -y git python python-pip
#
# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo dnf -y localinstall ./google-chrome-stable_current_x86_64.rpm
#
wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

#
# install ffmpeg
sudo mkdir /usr/local/ffmpeg
wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
sudo tar -xf /usr/local/ffmpeg/ffmpeg-git-amd64-static.tar.xz --output /usr/local/ffmpeg
sudo ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
#
# Download whisper yt AIJ
cd /~
git clone https://github.com/egrissino/whisper-youtube.git
#
# Install ppython dependencies
pip install git+https://github.com/openai/whisper.git yt-dlp
pip install yt-dlp
pip install -r ./whisper-youtube/requirements.txt
#
#