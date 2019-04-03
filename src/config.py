import json
import sys


config_loc = "configs/config.json"


# opens file, returns json dict, returns None if error
def load_config():
    try:
        with open(config_loc, "r") as f:
            return json.load(f)
    except Exception as e:
        print(e)
        sys.exit(1)


# opens file, writes config, returns True on success, False on error
def save_config(config):
    try:
        with open(config_loc, "w+") as f:
            json.dump(config, f, indent=4)

        return True
    except Exception as e:
        print(e)
        sys.exit(1)


# look for steamer in config, return True and idx, or False and None
def find_in_config(username, config):
    try:
        return config["streamers"].index(username)
    except ValueError:
        return None
