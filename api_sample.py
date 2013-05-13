from Project import ctlProject
from Job import ctlJob
from Execution import ctlExecution
from ctl_settings import *

if __name__ == "__main__":
    """
    print "test Project Class..."
    ctl_p = ctlProject("PPTV_LB")
    ctl_p.joblist2mongo()
    """
    print "test Job Class..."
    ctl_job = ctlJob("57")
    exec_id = ctl_job.ctl_job_run()
    ctl_exec = ctlExecution("57",exec_id)
    ctl_exec.get_exec_mongo_status()
