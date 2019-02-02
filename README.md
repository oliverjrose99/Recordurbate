# Recordurbate
The act of recording a Chaturbate live stream
## Requirements
* Python 3+
* Youtube-dl
* FFmpeg
## Installation
```commandline
wget https://github.com/oliverjrose99/Recordurbate/releases/download/1.2.0/recordurbate.tar
tar -xvf recordurbate.tar
cd recordurbate
chmod +x Recordurbate.py
```
The default config files will work out of the box with youtube-dl and FFmpeg installed. Streams will be saved to the folder videos/\<name>/\<name> \<date> \<hour>_\<min>.mp4. This can be changed by changing the youtube-dl.config file, see the configuration section for more. 
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
`youtube-dl_cmd`: The command to run youtube-dl or the location of the binary file.

`youtube-dl_config`: Location of the config file that is passed to youtube-dl with the parameter `--config-location`.

`auto_reload_config`: Sets whether or not to reload the config file after every loop. 
### Youtube-dl.config
This file is passed to youtube-dl with the parameter `--config-location`. See the [Youtube-dl Github](https://github.com/rg3/youtube-dl) for a full list of options and how to use them.
## TODO
* Better error messages and handling
* Proper daemonizing
