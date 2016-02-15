from .base_fitter import Fit
from scipy.stats import norm
import numpy

def _gaus_(x, *args):
    return  numpy.multiply(args[2],norm.pdf(numpy.divide(numpy.subtract(x,args[0]),args[1])))


class GausFit(Fit):
    def __init__(self, x,y,yerr=None, p0=[0, 2.0,1.0]):
        Fit.__init__(self, _gaus_, x,y,yerr, p0)
