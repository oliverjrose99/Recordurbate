import sys

from src.bot import Bot
from src.config import load_config, find_in_config, save_config


def usage():
    print("\nUsage: Recordurbate [add | del] username")
    print("       Recordurbate run\n")


def main():

    if len(sys.argv) == 3 and sys.argv[1] in ["add", "del"]:
        username = sys.argv[2].lower()

        # load and check config
        config = load_config()
        if config is None:
            return

        # look for streamer
        found, idx = find_in_config(username, config)

        if sys.argv[1] == "add":

            # if already added
            if found:
                print("{} has already been added".format(username))
                return

            # add streamer
            config["streamers"].append({"name": sys.argv[2], "recording": False})
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
        else:
            print("Could not save config")

    elif len(sys.argv) == 2 and sys.argv[1] == "run":
        bot = Bot()
        if not bot.error:
            bot.run()

    else:
        usage()
        return


if __name__ == "__main__":
    main()
