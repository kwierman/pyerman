"""
    :usage `from importROOT import ROOT`
    :warning This is bound to change in the future as the name is redundant and
    therefore it is bound to change.
"""
from subprocess import check_output
from sys import path

def rootConfig(*args):
    """
        Calls the root-config executable, if found
        :raises IOError Raised when  root-config not in path
    """
    cmd = ['root-config']
    for arg in args:
        cmd.append(arg)
    try:
        return check_output(cmd)
    except IOError:
        raise ImportError("""Could not import ROOT.
        Script: `root-config` not in path.
        Check to see if ROOT is installed""")

def rootHasPython():
    """
        Uses the root-config script to check if root was compiled with pyROOT.
    """
    ret = rootConfig('--has-python')
    return ret =='yes'

def rootFullConfig():
    """
        Returns a string of the full root config
    """
    return rootConfig('--config')

def rootFullLibDir():
    """
        Returns the full path of the root library root. The pyROOT module
        should be found here.
    """
    config = rootFullConfig()
    options = config.split()
    for opt in options:
        if 'libdir' in opt:
            if len(opt.split('='))>1:
                return opt.split("=")[1]
    if not rootHasPython():
        raise ImportError("ROOT not built with Python module")
    raise ImportError("Could Not Find ROOT LibDir")

try:
    import ROOT
except ImportError:
    path.append(rootFullLibDir())
    import ROOT
