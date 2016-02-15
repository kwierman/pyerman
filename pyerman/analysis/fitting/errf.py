from .base_fitter import Fit
from scipy.stats import norm
import numpy


def __errf__(x, *args):
    return  numpy.multiply(args[2],norm.cdf(numpy.divide(numpy.subtract(x,args[0]),args[1])))


class ErrfFit(Fit):
    def __init__(self, x,y,yerr=None, p0=[0, 2.0,1.0]):
        Fit.__init__(self, __errf__, p0, x,y,yerr)
