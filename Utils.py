from ctl_settings import *
import optparse,os,pymongo,sys,datetime,subprocess,time
from pymongo import Connection

class Utils(object):
    def __init__(self):
        pass
    @staticmethod
    def runCmd(command, timeout = 300):
        """call shell-command and either return its output or kill it
        if it doesn't normally exit within timeout seconds and return None
        """
        start = datetime.datetime.now()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while process.poll() is None:
            time.sleep(0.2)
            now = datetime.datetime.now()
            if (now - start).seconds > timeout:
                os.kill(process.pid, signal.SIGKILL)
                os.waitpid(-1, os.WNOHANG)
                return None
        return process.stdout.readlines()
