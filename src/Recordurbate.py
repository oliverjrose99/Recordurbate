#!/usr/bin/python3

import sys

from bot import Bot
from config import load_config, find_in_config, save_config


def usage():
    print("\nUsage: Recordurbate [add | del] username")
    print("       Recordurbate run")
    print("       Recordurbate list")
    print("       Recordurbate import list.txt")
    print("       Recordurbate export [file location]\n")


def main():

    if len(sys.argv) == 3 and sys.argv[1] in ["add", "del"]:
        # lower username, load config, look for streamer
        username = sys.argv[2].lower()
        config = load_config()
        found, idx = find_in_config(username, config)

        if sys.argv[1] == "add":

            # if already added
            if found:
                print("{} has already been added".format(username))
                return

            # add streamer
            config["streamers"].append(username)
            print("{} has been added".format(username))

        elif sys.argv[1] == "del":

            # if not yet added
            if not found:
                print("{} has not been added".format(username))
                return

            # remove streamer
            del config["streamers"][idx]
            print("{} has been deleted".format(username))

        if save_config(config):
            print("Done...")

    elif len(sys.argv) == 2 and sys.argv[1] == "run":
        bot = Bot()
        if not bot.error:
            bot.run()

    #list command - outputs the list of streamers - usage: ./Recordurbate.py list
    elif len(sys.argv) == 2 and sys.argv[1] == "list":
        config = load_config()
        print('Streamers in recording list:\n')
        for streamer in config['streamers']:
            print('- ' + streamer)

    #Import command - Imports streamers from a txt file - Usage: ./Recordurbate.py import list.txt
    elif len(sys.argv) == 3 and sys.argv[1] == "import":
        config = load_config()

        try:
            import_file = open(sys.argv[2], "r") #Open file to import
        except Exception as e:
            print('Could not open the import file.', e)

        for line in import_file: #For every username in the file
            username = line.rstrip() #Get username

            if username in config["streamers"]: #If username already exists, skip it
                pass
            else:
                config["streamers"].append(username) #If username does not exist, add it to the config

        if save_config(config): #Save config
            print('Done...')

    #Export command - Exports current streamer list as a file - Usage: ./Recordurbate.py export [file location] (Default location can be set in the config)
    elif len(sys.argv) >= 2 and sys.argv[1] == "export":
        config = load_config()

        if len(sys.argv) == 3:
            export_location = sys.argv[2] #If location is given, use it
        else:
            export_location = config["default_export_location"] #Else, use default location

        try:
            export_file = open(export_location, "w") #Open (or create) export file
        except Exception as e:
            print('Could not write to export location.', e)

        for streamer in config["streamers"]:
            export_file.write(streamer + '\n') #For every streamer in the config, write it to the file

        print('Done...') 

    else:
        usage()
        return


if __name__ == "__main__":
    main()
