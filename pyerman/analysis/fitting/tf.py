from .base_fitter import Fit
import numpy as np


def __tf_single__(E, *args):
    x = E+args[3]
    if args[1] == args[2]:
        return 1.e6
    elif x<args[0]:
        return 0.
    elif 1.0-(args[2]/args[1])*(x-args[0])/(x)<0:
        return 1.0
    elif x*(1.0-args[2]/args[1]) < args[0]:
        return 1.0-np.sqrt(1.0-(args[2]/args[1])*(x-args[0])/(x))
    else:
        return 1.0

def __tf__(X, *args):
    try:
        return [__tf_single__(x, *args) for x in X]
    except TypeError:
        return __tf_single__(X, *args)

class TFFit(Fit):
    def __init__(self, x,y,yerr=None, p0=[0, 2.0,1.0]):
        Fit.__init__(self, __tf__, p0, x,y,yerr )
