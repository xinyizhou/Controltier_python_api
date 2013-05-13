from ctl_settings import *
import optparse,os,pymongo,sys,datetime,subprocess,time
from pymongo import Connection
from xml.dom import minidom
from Utils import *

class ctlExecution(object):
    def __init__(self,job_id,exec_id):
        self.job_id = job_id
        self.exec_id = exec_id
        self.connection = Connection(CTL_MONGO_HOST,CTL_MONGO_PORT)
        self.db = self.connection["controltier"]
        self.coll_jobs = self.db["jobs"]
        self.coll_exec = self.db["executions"]
        self.coll_ctllog = self.db["logs"]
        self.prj_name = self.coll_jobs.find({"jobid":job_id}).limit(1)[0]["project"]
        get_file_cmd = "find %s -name %s|head -1" %(CTL_TXT_LOGDIR+self.prj_name,self.exec_id+".txt")
        self.txt_file = self.__exeCmd(get_file_cmd)[0].strip()

    def __exeCmd(self, cmd):
        return Utils.runCmd(cmd)

    def upload_log2mongo(self):
        f = open(self.txt_file)
        file_content = f.readlines()
        status = "succ"
        for line in file_content:
            self.coll_ctllog.insert({"project":self.prj_name,"jobid":self.job_id,"execid":self.exec_id,"logline":line.strip()})
            if "Remote command failed" in line:
                status = "fail"
            if "threw an exception" in line:
                status = "fail"
        f.close()
        return status

    def check_exec_status(self):
        tail_cmd = "tail -n1 %s" % self.txt_file
        job_start_time = datetime.datetime.now()
        exec_dict = {"jobid":self.job_id,"execid":self.exec_id,"starttime":job_start_time,"endtime":"","status":"running"}
        self.coll_exec.insert({'jobid':self.job_id,'execid':self.exec_id}, {"$set": exec_dict})
        while True:
            tail_result = self.__exeCmd(tail_cmd)[0].strip()
            if '^^^END^^^' in tail_result:
                job_end_time = datetime.datetime.now()
                print 'ctl job %s finished' % self.job_id
                exec_dict["endtime"] = job_end_time
                exec_dict["status"] = self.upload_log2mongo()
                self.coll_exec.update({'jobid':self.job_id,'execid':self.exec_id}, {"$set": exec_dict})
                break
            time.sleep(3)

    def get_exec_mongo_status(self):
        for i in self.coll_exec.find({"jobid":self.job_id,"execid":self.exec_id}):
            print i["starttime"],i["endtime"],i["status"]

