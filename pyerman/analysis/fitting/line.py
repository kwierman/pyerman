from .base_fitter import Fit
import numpy


def __line__(x, *args):
    return numpy.add(numpy.multiply(args[0],x) , args[1] )


class LineFit(Fit):
    def __init__(self, x,y,yerr=None, p0=[0, 2.0,1.0]):
        Fit.__init__(self, __line__,p0, x,y,yerr)
