
from . import ssh
def default_ssh(cmd):
    ssh()




def ssh(cmd):
    return ssh_proto("killdevil.unc.edu",cmd, "kwierman","Shivers75!")


def check_jobs():
    bjobs = ssh("bjobs")
    logging.info(bjobs)
    return "No unfinished job found" not in "".join(bjobs)

def check_jobs_struct():
    bjobs = ssh("bjobs")
    logging.info(bjobs)
    return [i.split() for i in bjobs.split("\r\n") if len(i)>0]

def peek_job(jobn):
    bpeek = ssh("bpeek {}".format(jobn))
    return bpeek

def submit_kassiopeia_job(filename, params={}):
    opt_string = " ".join([key+"="+value for key,value in params.iteritems()])
    cmd="bsub -q gpu Kassiopeia {} -r {}".format(filename, opt_string)
    logger.info(cmd)
    return ssh(cmd)

def scp(file_name, to):
    timeout=3600
    fname = tempfile.mktemp()
    fout = open(fname, 'w')
    scp_cmd = "scp killdevil.unc.edu:{} {}".format(file_name, to)
    logger.info(scp_cmd)
    child = pexpect.spawn(scp_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline("Shivers75!")
    child.logfile = fout
    child.expect(pexpect.EOF)
    child.close()
    fout.close()

    fin = open(fname, 'r')
    stdout = fin.read()
    fin.close()

    if 0 != child.exitstatus:
        raise Exception(stdout)
    return stdout

def remove(filename):
    cmd="rm {}".format(filename)
    logger.info(cmd)
    return ssh("killdevil.unc.edu",cmd, "kwierman","Shivers75!")
