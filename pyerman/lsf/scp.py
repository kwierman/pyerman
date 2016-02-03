import pexpect
import tempfile

def send(file_name, to, password):
    timeout=3600
    fname = tempfile.mktemp()
    fout = open(fname, 'w')
    scp_cmd = "scp {} {}".format(file_name, to)
    child = pexpect.spawn(scp_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline(password)
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
