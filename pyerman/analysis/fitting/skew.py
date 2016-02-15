from .base_fitter import Fit
from scipy.stats import norm
import numpy

def _skew_(x,args):
    t = numpy.divide(numpy.subtract(x,args[0]) , args[1] )
    return numpy.multiply(args[3], numpy.multiply( (2.0), numpy.multiply( norm.pdf(t), norm.cdf( numpy.multiply(args[2],t) ) ) ) )


class SkewFit(Fit):
    def __init__(self, x,y,yerr=None, p0=[0, 2.0,1.0]):
        Fit.__init__(self, _skew_, x,y,yerr, p0)
