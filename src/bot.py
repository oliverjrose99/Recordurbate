import signal
import subprocess

import os
import requests
import time

from config import load_config


class Bot:

    error = False
    running = True
    config = None
    processes = []

    logger = None

    def __init__(self, logger):
        self.logger = logger

        # load config
        self.reload_config()

        # reg signals
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, signum, stack):
        self.logger.info("Caught stop signal, stopping")
        self.running = False

    def reload_config(self):

        # if config not loaded at all
        if self.config is None:
            self.config = load_config()

            for idx, name in enumerate(self.config["streamers"]):
                # add info
                self.config["streamers"][idx] = [name, False]

            return

        # load new
        new_config = load_config()

        # remove all deleted streamers
        for idx, streamer in enumerate(self.config["streamers"]):
            if streamer[0] not in new_config["streamers"]:
                self.logger.info(streamer[0], "has been removed")
                del self.config["streamers"][idx]

        # add all new streamers
        for new_streamer in new_config["streamers"]:

            # find streamer
            found = False
            for streamer in self.config["streamers"]:
                if streamer[0] == new_streamer:
                    found = True

            # add if not found
            if not found:
                self.config["streamers"].append([new_streamer, False])

    def is_online(self, username):
        url = "https://chaturbate.com/get_edge_hls_url_ajax/"
        headers = {"X-Requested-With": "XMLHttpRequest"}
        data = {"room_slug": username, "bandwidth": "high"}

        try:
            r = requests.post(url, headers=headers, data=data)
            if r.json()["room_status"] == "public":
                return True

            return False

        except Exception as e:
            self.logger.info(e)
            return None

    def run(self):
        while self.running:
            
            # reload config
            if self.config["auto_reload_config"]:
                self.reload_config()

            # check current processes
            for idx, rec in enumerate(self.processes):

                # check if ended
                if rec[1].poll() is not None:
                    self.logger.info("Stopped recording", rec[0])

                    # set streamer recording to false
                    for loc, streamer in enumerate(self.config["streamers"]):
                        if streamer[0] == rec[0]:
                            self.config["streamers"][loc][1] = False

                    # remove from proc list
                    del self.processes[idx]

            # check to start recording
            for idx, streamer in enumerate(self.config["streamers"]):

                # if already recording
                if streamer[1]:
                    continue

                # check if online
                if self.is_online(streamer[0]):
                    self.logger.info("Started to record {}".format(streamer[0]))

                    # prep args
                    args = [self.config["youtube-dl_cmd"],  # youtube-dl bin
                            "https://chaturbate.com/{}/".format(streamer[0]),  # chaturbate url
                            "--config-location", self.config["youtube-dl_config"]]  # youtube-dl config
                    # append idx and process to processes list
                    self.processes.append([streamer[0], subprocess.Popen(args, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull)])

                    # set to recording
                    self.config["streamers"][idx][1] = True

            # wait 1 min in 1 second intervals
            for i in range(60):
                if not self.running:
                    break

                time.sleep(1)

        # loop ended, stop all recording
        for rec in self.processes:
            # send sigint, wait for end
            rec[1].send_signal(signal.SIGINT)
            rec[1].wait()
