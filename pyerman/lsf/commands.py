from . import ssh
from pyerman.table import Table
from . import config

def bjobs(local_config = None, timeout=30, bg_run=False):
    if local_config is None:
        local_config = config.getLSFConfigSingleton()
    return ssh.send('bjobs',local_config.server,
                    local_config.username,
                    local_config.password,
                    timeout,
                    bg_run)

def bjobs_table(local_config = None, timeout=30, bg_run=False):

    bj = bjobs(local_config, timeout, bg_run)
    struct = [i.split() for i in bj.split("\r\n") if len(i)>0]
    output = Table(struct[0], [])
    for line in struct[1:]:
        row = [line[0], line[1], line[2], line[3],line[4]]
        if len(line)>10:
            row.append(line[5])
            row.append(line[6]+" "+line[7])
            row.append(line[8]+" "+line[9]+" "+line[10])
        else:
            row.append('')
            row.append(line[5]+" "+line[6])
            row.append(line[7]+" "+line[8]+" "+line[9])
        output.insert_row(row)
    return output

def bpeek(jobn,local_config=None, timeout=30, bg_run=False):
    if local_config is None:
        local_config = config.getLSFConfigSingleton()
    return ssh.send('bpeek {}'.format(jobn),
                    local_config.server,
                    local_config.username,
                    local_config.password,
                    timeout,
                    bg_run)

def bkill(jobn,local_config=None, timeout=30, bg_run=False):
    if local_config is None:
        local_config = config.getLSFConfigSingleton()
    return ssh.send('bkill {}'.format(jobn),
                    local_config.server,
                    local_config.username,
                    local_config.password,
                    timeout,
                    bg_run)

def remove_file(filename,local_config=None, timeout=30, bg_run=False):
    if local_config is None:
        local_config = config.getLSFConfigSingleton()
    return ssh.send('rm {}'.format(filename),
                    local_config.server,
                    local_config.username,
                    local_config.password,
                    timeout,
                    bg_run)

def list_files(directory,local_config=None, timeout=30, bg_run=False):
    if local_config is None:
        local_config = config.getLSFConfigSingleton()
    return ssh.send('ls {}'.format(directory),
                    local_config.server,
                    local_config.username,
                    local_config.password,
                    timeout,
                    bg_run).strip('\r\n').split('\r\n')
