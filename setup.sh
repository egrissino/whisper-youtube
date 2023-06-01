#!/bin/bash
#
export RM=""
if type "yum" > /dev/null 2>&1; then
  export RM=yum
elif type "apt" > /dev/null 2>&1; then
  export RM=apt
elif type "dnf" > /dev/null 2>&1; then
  export RM=ydnf
fi
#
if [[ $RM != "" ]]; then
  # update and install deps
  sudo $RM update
  sudo $RM install -y git python3 python3-pip unzip cuda-toolkit-12-1
  #
  # Install Chrome
  if ! type "google-chrome" > /dev/null 2>&1; then
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
    sudo $RM -y localinstall ./google-chrome-stable_current_x86_64.rpm
  fi
  #
fi
#
if ! type "chromedriver" > /dev/null 2>&1; then
  wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip
  unzip chromedriver_linux64.zip
fi
#
# install ffmpeg
if ! type "ffmpeg" > /dev/null 2>&1; then
  sudo mkdir /usr/local/bin/ffmpeg/
  wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
  sudo tar -xf ./ffmpeg-git-amd64-static.tar.xz
  sudo cp -r ./ffmpeg-git-20230313-amd64-static/* /usr/local/bin/ffmpeg/
  sudo ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
fi
#
# Download whisper yt AIJ
git clone https://github.com/egrissino/whisper-youtube.git
#
# Install ppython dependencies
pip3 install git+https://github.com/openai/whisper.git yt-dlp
pip3 install -r ./whisper-youtube/requirements.txt
#
#
