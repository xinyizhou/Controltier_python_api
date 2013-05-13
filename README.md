Controliter Python API
----
Controliter is an open source build and deployment automation framework. Controliter doucment:http://doc36.controltier.org/wiki/Main_Page
----
#API example
from Controltier.Project import ctlProject

from Controltier.Job import ctlJob

from Controltier.Execution import ctlExecution

#Project API

prj = ctlProject("PRJ_NAME")

prj.create_project()   #create controliter project
prj.get_HostIpTag_list() # print project,ip,hostname,tag

prj.add_host(hostname,tag,ctl_user,ip)   #add host to project

prj.del_host(ip)   #delete host from project

prj.joblist2mongo()   # sync joblist to mongodb

#JOB API

ctl_job = ctlJob("job_id")

ctl_job.ctl_job_run()   

 

#Execution API

ctl_exec = ctlExecution(job_id,exec_id)  

ctl_exec.check_exec_status()  

ctl_exec.get_exec_mongo_status()  
