import numpy as np
from scipy.optimize import leastsq, nnls, curve_fit
import scipy.stats as stats


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
        self.p1, self.pcov = curve_fit(self.fn, self.x, self.y, p0= self.p0, sigma=yerr)
        self.chisquare,self.pvalue = stats.chisquare(self.y, f_exp=self.y1, ddof=len(self.p1), axis=0)

    def __fn__(self, x):
        return self.fn(x, *self.p1)

    @property
    def parerror(self):
        return np.sqrt(np.diag(self.pcov))

    @property
    def y1(self):
        return [self.__fn__(i) for i in self.x]

    @property
    def DF(self):
        return len(self.x)-len(self.p1)

    @property
    def t(self):
        # 95% C.L. conversion factor
        return stats.t.ppf(0.95, self.DF )

    @property
    def residuals(self):
        return np.subtract(self.y, self.y1 )

    @property
    def s_err(self):
        return np.sqrt(np.sum(np.power(self.residuals,2))/(self.DF))

    def CI(self, x2):
        return self.t*self.s_err*np.sqrt(1/len(self.x)+np.subtract(x2,np.mean(self.x))**2/np.sum(np.subtract(self.x,np.mean(self.x))**2))

    def PI(self, x2):
        return self.t*self.s_err*np.sqrt(1+1/len(self.x)+(x2-np.mean(self.x))**2/np.sum((self.x-np.mean(self.x))**2))
