from ctl_settings import *
import optparse,os,pymongo,sys,datetime,subprocess,time
from pymongo import Connection
from xml.dom import minidom
from Utils import *

class ctlProject(object):
    def __init__(self,prj_name):
        self.prj_name = prj_name
        self.resource_xml = CTL_PROJECT_DIR + self.prj_name + "/etc/resources.xml"

    def __exeCmd(self, cmd):
        return Utils.runCmd(cmd)

    def create_project(self):
        if os.path.isfile(self.resource_xml):
            print "Project %s existed, please remove it first" % self.prj_name
            sys.exit(0)
        create_cmd =  "export CTL_BASE=/usr/local/ctier/ctl;%s -p %s --action create" % (CTL_PROJECT,self.prj_name)
        print self.__exeCmd(create_cmd)

    def project_xml2mongo(self):
        if not os.path.isfile(self.resource_xml):
            print "Project %s not existed, please create it first" % self.prj_name
            sys.exit(0)
        f = open(self.resource_xml)
        dom = minidom.parse(f)
        root = dom.documentElement
        nodes = root.getElementsByTagName("node")
        connection = Connection(CTL_MONGO_HOST,CTL_MONGO_PORT)
        db = connection["controltier"]
        coll = db["project_host_info"]
        coll.remove({"project":self.prj_name})
        for node in nodes:
            ip =  node.getAttribute("hostname")
            hostname =  node.getAttribute("name")
            tag = node.getAttribute("tags")
            if tag == "" or tag == "deleted":
                continue
            else:
                coll.insert({"project":self.prj_name,"ip":ip,"hostname":hostname,"tag":tag})
        f.close()

    def get_HostIpTag_list(self):
        self.project_xml2mongo()
        connection = Connection(CTL_MONGO_HOST,CTL_MONGO_PORT)
        db = connection["controltier"]
        coll = db["project_host_info"]
        for i in coll.find({"project":self.prj_name}):
            print i["project"],i["ip"],i["hostname"],i["tag"]

    def add_host(self,hostname,tag,ctl_user,ip):
        if not os.path.isfile(self.resource_xml):
            print "Project %s not existed, please create it first" % self.prj_name
            sys.exit(0)
        os.popen("mkdir -p "+WORK_DIR)
        os.chdir(WORK_DIR)
        print "[PPTV Controliter API]====Adding %s to Project %s ====" % (ip,self.prj_name)
        tmp_xml = WORK_DIR + self.prj_name + ".xml"
        os.popen(">%s" % tmp_xml)
        f = open(tmp_xml,'aw+')
        f.write(HOST_XML_HEADER)
        f.write(HOST_XML_BODY % (hostname,tag,ctl_user,ip))
        f.write(HOST_XML_FOOTER)
        f.close()
        add_host_cmd = "export CTL_BASE=/usr/local/ctier/ctl;%s -p %s -m ProjectBuilder -c load-resources -- -filename %s" % (CTL_BIN,self.prj_name,tmp_xml)
        print "".join(self.__exeCmd(add_host_cmd))
        self.project_xml2mongo()

    def del_host(self,ip):
        self.project_xml2mongo()
        connection = Connection(CTL_MONGO_HOST,CTL_MONGO_PORT)
        db = connection["controltier"]
        coll = db["project_host_info"]
        count = coll.find({"project":self.prj_name,"ip":ip}).count()
        if count > 0:
            tmp_xml = WORK_DIR + self.prj_name + ".xml"
            os.popen(">%s" % tmp_xml)
            f = open(tmp_xml,'aw+')
            f.write(HOST_XML_HEADER)
            for j in coll.find({"project":self.prj_name,"ip":ip}):
                f.write(HOST_XML_BODY % (j["hostname"],"deleted","root",j["ip"]))
            f.write(HOST_XML_FOOTER)
            f.close()
            del_host_cmd = "export CTL_BASE=/usr/local/ctier/ctl;%s -p %s -m ProjectBuilder -c load-resources -- -filename %s" % (CTL_BIN,self.prj_name,tmp_xml)
            print "".join(self.__exeCmd(del_host_cmd))
        else:
            print "No such ip:%s in Project %s,please check." % (ip,self.prj_name)
        self.project_xml2mongo()

    def joblist2mongo(self):
        if not os.path.isfile(self.resource_xml):
            print "Project %s not existed, please create it first" % self.prj_name
            sys.exit(0)
        project = self.prj_name
        tmp_xml = WORK_DIR + project + "_job.xml"
        save_job_cmd = "export CTL_BASE=/usr/local/ctier/ctl;%s -p %s save -f %s" % (CTL_JOBS,project,tmp_xml)
        save_rst = self.__exeCmd(save_job_cmd)
        f = open(tmp_xml)
        dom = minidom.parse(f)
        root = dom.documentElement
        jobs = root.getElementsByTagName("job")
        connection = Connection(CTL_MONGO_HOST,CTL_MONGO_PORT)
        db = connection["controltier"]
        coll = db["jobs"]
        coll.remove({"project":project})
        for job in jobs:
            result = {}
            result["project"] = project
            node_id  =  job.getElementsByTagName( "id" )[0]
            node_name = job.getElementsByTagName( "name" )[0]
            job_id = node_id.childNodes[0].nodeValue
            job_nodename = node_name.childNodes[0].nodeValue
            if len(job.getElementsByTagName( "group" )) > 0:
                node_group = job.getElementsByTagName( "group" )[0]
                job_nodename = "(" + node_group.childNodes[0].nodeValue +  ")" + node_name.childNodes[0].nodeValue
            result["jobid"] = job_id
            result["jobname"] = job_nodename
            coll.insert(result)
        f.close()