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
        # Fixes issue #69 "Failed when calling is_online(..), new API url available."
        # See the link below for full list of API parameters (gender, region, tag, limit, offset, etc..)
        # Official Chaturbate API https://chaturbate.com/affiliates/promotools/api_usersonline/
        # Special thanks to https://www.blackhatworld.com/seo/chaturbate-api.1028000/page-2#post-11041420
        
        # With this API url, cam username must be in the first 500 results in order to be current_show="public" to be verified, due to max limit=500
        # offset=(any non-negative number) can be included to obtain more results beyond the first 500.
        MAX_API_RESULTS = "500" 
        url = "https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=DkfRj&client_ip=request_ip&limit=" + MAX_API_RESULTS

        try:
            time.sleep(3)  # fix issue 30
            r = requests.get(url)
            results =  r.json()["results"]
            
            self.logger.debug(r)
            self.logger.debug(results)
            
            for result in results:
                if result["username"] == username and result["current_show"] in ["public"]:
                    return True

            return False

        except Exception as e:
            self.logger.exception("Exception: call to is_online(..) failed.")
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
