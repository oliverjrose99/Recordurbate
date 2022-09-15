#
# Thanks to: https://web.archive.org/web/20131017130434/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
#

import atexit
import logging
import os
import sys
import time

from signal import SIGTERM
from bot import Bot

class Daemon:

    pid = None
    pidfile = "./configs/rb.pid"
    logfile = "./configs/rb.log"

    def __init__(self):
        # setup logger
        self.logger = logging.getLogger("Recordurbate")
        self.logger.setLevel(logging.DEBUG)
        
        fh = logging.FileHandler(self.logfile)
        fh.setLevel(logging.DEBUG)

        FORMAT = "[%(asctime)s %(filename)s:%(lineno)s - %(funcName)s()]- %(message)s"
        fh.setFormatter(logging.Formatter(FORMAT))
        self.logger.addHandler(fh)

    def daemonize(self):
        self.logger.info("Starting daemon")
        self.logger.debug("calling os.fork()")

        # double fork
        try:
            # Note: os.fork() "returns 0 in the child process and child’s process id in the parent process".
            # See https://www.geeksforgeeks.org/python-os-fork-method/
            pid = os.fork()
            if pid > 0:
                self.logger.debug("Parent PID = {}".format(os.getpid()))
                sys.exit(0)
            
            pid = os.fork()
            if pid > 0:
                self.logger.debug("Fork PID = {}".format(os.getpid()))
                sys.exit(0)
            
                self.logger.debug("Double Fork PID = {} - fully daemonized".format(os.getpid()))

        except Exception as e:
            # Issue #65 - os.fork() fails in Windows but it does not throw OSError which bypassed the catch block. Resolved issue by changing "OSError" to "Exception".
            self.logger.exception("Failed to daemonize, {}. ".format(e))
            print("Failed to daemonize. Note: run recordurbate on Linux terminal instead of Windows. See " + logfile + " for details.")
            sys.exit(1)

        # close std's
        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()

        # write pid file
        self.pid = os.getpid()
        with open(self.pidfile, "w+") as pf:
            pf.write("{}\n".format(self.pid))
        
        # register remove
        atexit.register(os.remove, self.pidfile)

        self.logger.info("Successfully started daemon, pid: {}".format(self.pid))

    def read_pid(self):
        try:
            with open(self.pidfile) as pf:
                return int(pf.read().strip())

        except IOError:
            return None

    def start(self):
        # check pid file
        pid = self.read_pid()

        # if found, exit
        if pid:
            print("Pid file found, is Recordurbate already running? pid: {}".format(pid))
            sys.exit(1)

        # continue
        self.daemonize()
        self.run(self.logger)

    def stop(self):
        # check pid file
        pid = self.read_pid()

        if not pid:
            print("Pid file not found, Daemon not running?")
            return

        # try and kill
        try:
            while True:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)

        # when excepts, check process died
        except OSError as e:
            e = str(e)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            
            else:
                print("Error killing process, {}".format(e))
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self, logger):
        bot = Bot(logger)
        if not bot.error:
            bot.run()
