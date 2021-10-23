import os
import signal
import subprocess
import time

import requests
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
        if self.running:
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
                self.logger.info("{} has been removed".format(streamer[0]))
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
            time.sleep(3)  # fix issue 30
            r = requests.post(url, headers=headers, data=data)
            if r.json()["room_status"] == "public":
                return True

            return False

        except Exception as e:
            self.logger.exception(e)
            return None

    def run(self):
        while self.running:
            
            # debug
            try:

                # reload config
                if self.config["auto_reload_config"]:
                    self.reload_config()

                # check current processes
                for idx, rec in enumerate(self.processes):

                    # check if ended
                    if rec[1].poll() is not None:
                        self.logger.info("Stopped recording {}".format(rec[0]))

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

                        # prep args (dl bin and config)
                        args = self.config["youtube-dl_cmd"].split(" ") + ["https://chaturbate.com/{}/".format(streamer[0]), "--config-location", self.config["youtube-dl_config"]] 
                        
                        # append idx and process to processes list
                        self.processes.append([streamer[0], subprocess.Popen(args, 0)])

                        # set to recording
                        self.config["streamers"][idx][1] = True
                    
                    # check rate limit
                    if self.config["rate_limit"]:
                        time.sleep(self.config["rate_limit_time"])

                # wait 1 min in 1 second intervals
                for i in range(60):
                    if not self.running:
                        break

                    time.sleep(1)
                
            except Exception:
                self.logger.exception("loop error")
                time.sleep(1)

        # loop ended, stop all recording
        for rec in self.processes:
            # send sigint, wait for end
            rec[1].send_signal(signal.SIGINT)
            rec[1].wait()
        
        self.logger.info("Successfully stopped")
