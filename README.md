# Recordurbate
The act of recording a Chaturbate live stream
## Requirements
* Linux
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
The default config files will work out of the box with youtube-dl and FFmpeg installed. Streams will be saved to the folder videos/\<name>/\<name> \<date> \<hour>_\<min>.mp4. This can be changed by editing the youtube-dl.config file, see the configuration section for more. 
## Usage

View the usage/help text
```
./Recordurbate help
```

Add or remove a streamer to record
```
./Recordurbate.py [add | del] username
```

Start, stop or restart the daemon
```
./Recordurbate.py [start | stop | restart]
```

List the streamers in the config
```
./Recordurbate list
```

Import streamers from a file
```
./Recordurbate import [file]
```

Export streamers to a file. The file parameter is optional and the default location will be used if not passed
```
./Recordurbate.py export [file]
```

## Config Files
There are two main config files that are used, `config.json` and `youtube-dl.config`, both being stored in the configs directory. In that directory is also the log file (rb.log) and the pid file (rb.pid).

### Config.json
This file is used directly by Recordurbate and contains all the configuration options as well as the array of streamers to record.

`youtube-dl_cmd` - Sets the command used to run Youtube-dl. 

`youtube-dl_config` - Sets where the config file for Youtube-dl is located and is passed with the `--config-location` parameter. Note that system and user wide configs still apply, see [this link](https://github.com/ytdl-org/youtube-dl#configuration) for more info.

`auto_reload_config` - Sets if the bot should reload the config after every loop to allow adding or removing streamers while running.

`default_export_location` - Sets the default location for the export command.

`streamers` - An array of strings, each of which is a streamer to record.

## Youtube-dl.config
This file is used to set all of the Youtube-dl config options and is passed using the `--config-location` parameter. As mentioned, the system and user wide configs still apply. Options such as quality, export options and more can be [found on the Youtube-dl Github.](https://github.com/ytdl-org/youtube-dl)

## TODO and future features
* Integration with Chaturbate e.g. import from following, record paid for shows, etc
* Better logging and config options
* Support for other sites
* Check if a streamer exists or not
* And MORE!!!

## Notes

### Recordings lag and freeze
A couple users have reported that recordings may lag and freeze which was due to out of date youtube-dl and ffmpeg versions. If you experience this, please ensure you are using the latest stable versions and that your internet, storage and CPU are not bottlenecks causing issues.

### No files / Not running
Some users found that no files were being made which was due to either software not being installed/configured or incorrect permissions. It also possible that AppArmor is blocking the script which can be checked by looking at the syslog. Please check these before making an issue.

### Large Files and bandwidth usage
Because the streams are indented to be watched live, there is little compression on the video. This can cause very large files and heavy internet usage as the max settings for some streamers are 4k/60fps and youtube-dl defaults to best available options. Internet usage can be reduced by using a lower quality and file size can be further reduced by compressing the file (will causes heavy CPU usage). All this can be done with youtube-dl config options. 