import numpy as np
from scipy.optimize import leastsq, nnls, curve_fit
from scipy.stats import norm, chisquare

class Fit(object):
    """
        Inherit from this in order to obtain some object oriented fitting
    """

    def __init__(self, fn, p0,x,y,yerr=None):
        self.fn = fn
        self.x = x
        self.y = y
        self.yerr = yerr
        self.p0 = p0
    def __fn__(self, x):
        return self.fn(x, *self.p1)
    def do(self):
        self._fit_()
        self._chi2_()
    def _fit_(self):
        self.p1, self.pcov = curve_fit(self.fn, self.x, self.y, p0= self.p0)
    def _chi2_(self):
        self.x2,self.pvalue = chisquare(self.y, f_exp=[self.__fn__(i) for i in x], ddof=len(self.p1), axis=0)
