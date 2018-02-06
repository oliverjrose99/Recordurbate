# Recordurbate
The act of recording a Chaturbate live stream
## Requirements
* Python 3+
* Youtube-dl
* FFmpeg
## Installation
```commandline
wget https://github.com/oliverjrose99/Recordurbate/releases/download/1.0.0/Recordurbate.tar
tar -xvf Recordurbate.tar
cd Recordurbate
chmod +x Recordurbate.py
```
## Usage
To add or delete users to record, use the command:
```
./Recordurbate.py [add | del] username
```
To start the bot, use the following command. I would recommend using this at first to ensure that your youtube-dl and FFmpeg configurations work as intended and don't have any issues.
```commandline
./Recordurbate.py run
```
Currently the bot will not daemonize it's self, so use the following command to do so until implemented:
```commandline
nohup ./Recordurbate.py run &
```
## Configuration
Currently the configs folder contains two files by default, config.json and youtube-dl.config.
###  Config.json
This file contains which streamers should be recorded as well as the locations of the youtube-dl binary and its config file. The two locations can be absolute or relative to the Recordurbate.py file. By default it will use the command "youtube-dl" and pass the file in the configs folder.
### Youtube-dl.config
This file is passed to youtube-dl with the parameter `--config-location`. See the [Youtube-dl Github](https://github.com/rg3/youtube-dl) for a full list of options and how to use them.
## TODO
* Better error messages and handling
* Proper daemonizing