"""
    :usage `from importROOT import ROOT`
    :warning This is bound to change in the future as the name is redundant and
    therefore it is bound to change.
"""
from subprocess import check_output
from sys import path

def rootConfig(*args):
    cmd = ['root-config']
    for arg in args:
        cmd.append(arg)
    try:
        return check_output(cmd)
    except IOError:
        raise IOError("root-config not found")

def rootHasPython():
    ret = rootConfig('--has-python')
    return ret =='yes'

def rootFullConfig():
    return rootConfig('--config')

def rootFullLibDir():
    config = rootFullConfig()
    options = config.split()
    for opt in options:
        if 'libdir' in opt:
            try:
                return opt.split("=")[1]
            except IndexError:
                continue
    raise ValueError("Could Not Find ROOT LibDir")

try:
    import ROOT
except ImportError:
    path.append(rootFullLibDir())
    import ROOT
