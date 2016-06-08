import tempfile
import pexpect

def send(cmd,host=None,user=None, password=None, timeout=30, bg_run=False):
    """SSH'es to a host using the supplied credentials and executes a command.
    Throws an exception if the command doesn't return 0.
    bgrun: run command in the background"""

    temp = tempfile.TemporaryFile()

    options = '-q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -oPubkeyAuthentication=no'
    if bg_run:
        options += ' -f'
    ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)
    child = pexpect.spawn(ssh_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline(password)
    child.logfile = temp
    child.expect(pexpect.EOF)
    child.close()


    temp.seek(0)
    stdout = temp.read()
    temp.close()

    if 0 != child.exitstatus:
        raise Exception(stdout)
    return stdout

def scp_send(src_filepath, dest_filepath,host=None,user=None, password=None, timeout=3600, bg_run=False):
    """SSH'es to a host using the supplied credentials and executes a command.
    Throws an exception if the command doesn't return 0.
    bgrun: run command in the background"""

    temp = tempfile.TemporaryFile()

    scp_cmd = "scp {} {}@{}:{}".format(src_filepath, user, host, dest_filepath)
    child = pexpect.spawn(scp_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline(password)
    child.logfile = temp
    child.expect(pexpect.EOF)
    child.close()
    temp.seek(0)
    stdout = temp.read()
    temp.close()

    if 0 != child.exitstatus:
        raise Exception(stdout)
    return stdout


def scp_get(src_filepath, dest_filepath,host=None,user=None, password=None, timeout=30, bg_run=False):
    """SSH'es to a host using the supplied credentials and executes a command.
    Throws an exception if the command doesn't return 0.
    bgrun: run command in the background"""

    temp = tempfile.TemporaryFile()
    scp_cmd = "scp {}@{}:{} {}".format(user, host, dest_filepath, src_filepath)
    child = pexpect.spawn(scp_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline(password)
    child.logfile = temp
    child.expect(pexpect.EOF)
    child.close()
    temp.seek(0)
    stdout = temp.read()
    temp.close()

    if 0 != child.exitstatus:
        raise Exception(stdout)
    return stdout
