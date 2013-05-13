from ctl_settings import *
import optparse,os,pymongo,sys,datetime,subprocess,time
from pymongo import Connection
from xml.dom import minidom
from Utils import *

class ctlJob(object):
    def __init__(self,job_id):
        if self.__is_valid_jobid(job_id):
            self.jobid = job_id
        else:
            print "%s is not a valid JOBID,Please Check!" % job_id
            sys.exit(0)

    def __is_valid_jobid(self,jobid):
        connection = Connection(CTL_MONGO_HOST,CTL_MONGO_PORT)
        db = connection["controltier"]
        coll = db["jobs"]
        joblist = coll.distinct("jobid")
        if jobid in joblist:
            return True
        else:
            return False

    def __exeCmd(self, cmd):
        return Utils.runCmd(cmd)

    def ctl_job_run(self,*args,**kwargs):
        job_id = self.jobid
        run_job_cmd = "export CTL_BASE=/usr/local/ctier/ctl;%s -i %s" %(CTL_RUN,job_id)
        if len(args) > 0:
            run_job_cmd += " --"
            for k in kwargs.keys():
                run_job_cmd += " -%s %s" % (k,kwargs[k])
        run_rst = self.__exeCmd(run_job_cmd)
        exec_id = run_rst[1].split(" ")[0].strip("[]")
        print "Execution ID:",exec_id
        bg_exec_status_check = "nohup %s %s %s &>/dev/null &" % (BG_EXEC_STATUS_CHECK,self.jobid,exec_id)
        print bg_exec_status_check
        bg_status = self.__exeCmd(bg_exec_status_check)
        return exec_id

    def ctl_run_with_args(self,command_args):
        print command_args

