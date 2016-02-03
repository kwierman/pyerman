from . import ssh
from pyerman.table import Table

def bjobs(host=None,user=None, password=None, timeout=30, bg_run=False):
    return ssh.send('bjobs',host,user, password, timeout, bg_run)

def bjobs_table(host=None,user=None, password=None, timeout=30, bg_run=False):
    bj = bjobs(host,user, password, timeout, bg_run)
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

def bpeek(jobn,host=None,user=None, password=None, timeout=30, bg_run=False):
    return ssh.send('bpeek',host,user, password, timeout, bg_run)

def remove_file(filename,host=None,user=None, password=None, timeout=30, bg_run=False):
    return ssh.send('rm {}'.format(filename),host,user, password, timeout, bg_run)

def list_files(directory, host=None,user=None, password=None, timeout=30, bg_run=False):
    return ssh.send('ls {}'.format(directory),host,user, password, timeout, bg_run)
