#!/usr/bin/python3

import sys

from bot import Bot
from config import load_config, find_in_config, save_config


def usage():
    print("\nUsage: Recordurbate [add | del] username")
    print("       Recordurbate run\n")


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

    else:
        usage()
        return


if __name__ == "__main__":
    main()
