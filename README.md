# Recordurbate
The act of recording a Chaturbate live stream
## Requirements
* Python 3+
* Youtube-dl
* FFmpeg
## Installation
```commandline
wget TODO: latest release
unzip
cd Recordurbate
chmod +x Recordurbate.py
```
## Usage
To add or delete users to record, use the command:
```
./Recordurbate.py [add | del] username
```
To start the bot, use the following command. I would recommend using this at first to ensure that your youtube-dl and FFmpeg configurations work at intended and don't have any issues.
```commandline
./Recordurbate.py run
```
Currently the bot will not daemonize it's self, so use the following command to do so until implemented:
```commandline
nohup ./Recordurbate.py run &
```