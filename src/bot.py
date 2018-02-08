import signal
import subprocess

import requests
import time

from config import load_config


class Bot:

    error = False
    running = True
    config = None
    processes = []

    def __init__(self):

        # load config
        self.config = load_config()
        if self.config is None:
            self.error = True
            return

        # reg signals
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def stop(self, signum, stack):
        self.running = False

    def reload(self, signum, stack):
        # todo: implement
        return

    @staticmethod
    def is_online(username):
        url = "https://chaturbate.com/get_edge_hls_url_ajax/"
        headers = {"X-Requested-With": "XMLHttpRequest"}
        data = {"room_slug": username, "bandwidth": "high"}

        try:
            r = requests.post(url, headers=headers, data=data)
            if r.json()["room_status"] == "public":
                return True

            return False

        except Exception as e:
            print(e)
            return None

    def run(self):
        while self.running:

            # check current processes
            for idx, rec in enumerate(self.processes):

                # check if ended
                if rec[1].poll() is not None:
                    print("{} has stopped streaming".format(self.config["streamers"][rec[0]]["name"]))

                    # set not recording, remove from processes
                    self.config["streamers"][rec[0]]["recording"] = False
                    del self.processes[idx]

            # check to start recording
            for idx, streamer in enumerate(self.config["streamers"]):

                # if already recording
                if streamer["recording"]:
                    continue

                if self.is_online(streamer["name"]):
                    print("Starting to record", streamer["name"])

                    # prep args
                    args = [self.config["youtube-dl_cmd"],  # youtube-dl bin
                            "https://chaturbate.com/{}/".format(streamer["name"]),  # chaturbate url
                            "--config-location", self.config["youtube-dl_config"]]  # youtube-dl config
                    # append idx and process to processes list
                    self.processes.append([idx, subprocess.Popen(args,
                                                                 stdin=subprocess.DEVNULL,
                                                                 stdout=subprocess.DEVNULL,
                                                                 stderr=subprocess.DEVNULL)])

                    # set to recording
                    self.config["streamers"][idx]["recording"] = True

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
