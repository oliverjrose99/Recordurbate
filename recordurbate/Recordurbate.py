#!/usr/bin/python3
import sys
from daemon import Daemon
import config as Config

def usage():
    print("\nUsage: Recordurbate [add | del] username")
    print("       Recordurbate [start | stop | restart]")
    print("       Recordurbate list")
    print("       Recordurbate import list.txt")
    print("       Recordurbate export [file location]\n")
    print("       Recordurbate help\n")

def check_num_args(num):
    if len(sys.argv) != num:
        usage()
        return False
    
    return True

def add():
    if not check_num_args(3): return

    # load config and others
    config = Config.load_config()
    username = sys.argv[2].lower()
    idx = Config.find_in_config(username, config)

    # if already added
    if idx:
        print("{} has already been added".format(username))
        return

    # add and save
    config["streamers"].append(username)
    if Config.save_config(config):
        print("{} has been added".format(username))

def remove():
    if not check_num_args(3): return
    
    # load config and others
    config = Config.load_config()
    username = sys.argv[2].lower()
    idx = Config.find_in_config(username, config)

    # if not in list
    if idx == None:
        print("{} hasn't been added".format(username))
        return

    # delete and save
    del config["streamers"][idx]
    if Config.save_config(config):
        print("{} has been deleted".format(username))

def list_streamers():
    if not check_num_args(2): return

    # load config, print streamers
    config = Config.load_config()
    print('Streamers in recording list:\n')
    for streamer in config['streamers']:
        print('- ' + streamer)

def import_streamers():
    if not check_num_args(3): return

    # load config
    config = Config.load_config()
    
    # open and loop file
    with open(sys.argv[2], "r") as f:
        for line in f:
            username = line.rstrip()

            # if already in, print, else append
            if username in config["streamers"]:
                print("{} has already been added".format(username))
            else:
                config["streamers"].append(username)
    
    # save config
    if Config.save_config(config):
        print("Streamers imported, Config saved")

def export_streamers():
    if len(sys.argv) not in (2, 3): return usage()

    # load config
    config = Config.load_config()
    export_location = config["default_export_location"]

    # check export loc
    if len(sys.argv) == 3:
        export_location = sys.argv[2]

    # write file
    with open(export_location, "w") as f:
        for streamer in config["streamers"]:
            f.write(streamer + "\n")
    
    print("Written streamers to file")

def bot():
    if not check_num_args(2): return
    
    # make daemon inst
    daemon = Daemon()

    # start, stop or restart
    if sys.argv[1] == "start":
        daemon.start()
    
    elif sys.argv[1] == "stop":
        daemon.stop()
    
    elif sys.argv[1] == "restart":
        daemon.restart()

argument_map = {
    "help": usage,
    "add": add,
    "del": remove,
    "list": list_streamers,
    "import": import_streamers,
    "export": export_streamers,
    "start": bot, "stop": bot, "restart": bot
}

if __name__ == "__main__":
    try:
        func = argument_map.get(sys.argv[1], usage)
        func()
    except SystemExit: # prevents usage showing twice when starting
        pass
    except:
        usage()
