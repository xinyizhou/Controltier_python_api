CTL_INSTALL_DIR = '/usr/local/ctier/'
CTL_PROJECT_DIR = CTL_INSTALL_DIR + 'ctl/projects/'
CTL_PROJECT = CTL_INSTALL_DIR + 'pkgs/ctl-3.6.1/bin/ctl-project'
CTL_BIN = CTL_INSTALL_DIR + "pkgs/ctl-3.6.1/bin/ctl"
CTL_JOBS = CTL_INSTALL_DIR + "pkgs/ctl-3.6.1/bin/ctl-jobs"
CTL_RUN = CTL_INSTALL_DIR + "pkgs/ctl-3.6.1/bin/ctl-run"
CTL_MONGO_HOST = "127.0.0.1"
CTL_MONGO_PORT = 27002
WORK_DIR = "/home/tools/tmp/ctl_api_wrkdir/"
HOST_XML_HEADER = """
<!DOCTYPE project PUBLIC
"-//ControlTier Software Inc.//DTD Project Document 1.0//EN" "project.dtd">
<project>
"""
HOST_XML_BODY = """
<node type="Node" name="%s" description="" tags="%s" ctlBase="" ctlHome="" ctlUsername="%s" osFamily="unix" osName="Linux" osArch="x86_64" osVersion="" hostname="%s"/>
"""
HOST_XML_FOOTER = """
</project>
"""
CTL_TXT_LOGDIR = "/usr/local/ctier/ctl/var/logs/ctlcenter/"
BG_EXEC_STATUS_CHECK = "/home/tools/home/xinyizhou/controltier_test/70_66_ctl/bg_exec_status_check.py"