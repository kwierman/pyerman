from .base_fitter import Fit
from scipy.stats import norm
import numpy


def __errf__(x, *args):
    i1 = args[2]
    i2 = norm.cdf(numpy.divide(numpy.subtract(x, args[0]), args[1]))
    return numpy.multiply(i1, i2)


class ErrfFit(Fit):
    def __init__(self, x, y, yerr=None, p0=[0, 2.0, 1.0]):
        params = ['$\mu$', '$\sigma$', '$a$']
        Fit.__init__(self, __errf__, p0, x, y, yerr, params)
