from .base_fitter import Fit
import numpy


def __log__(x, *args):
    # inner_product = numpy.multiply(args[1], numpy.log(numpy.add(x, args[2])))
    a1 = numpy.add(x, args[2])
    a2 = numpy.divide(args[1], a1)
    a3 = numpy.add(args[0], a2)
    return a3
    # return numpy.add(args[0], inner_product)


class LogFit(Fit):
    def __init__(self, x, y, yerr=None, p0=[0, 2.0, 1.0]):
        Fit.__init__(self, __log__, p0, x, y, yerr)
