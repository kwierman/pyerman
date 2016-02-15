import numpy as np
from scipy.optimize import leastsq, nnls, curve_fit
from scipy.stats import chisquare, t


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
        self.p1, self.pcov = curve_fit(self.fn, self.x, self.y, p0= self.p0)
        self.x2,self.pvalue = chisquare(self.y, f_exp=self.y1, ddof=len(self.p1), axis=0)

    def __fn__(self, x):
        return self.fn(x, *self.p1)

    @property
    def parerror(self):
        return np.sqrt(np.diag(self.pcov))

    @property
    def y1(self):
        return [self.__fn__(i) for i in self.x]

    def CI(self, x2):
        DF = len(self.x)-len(self.p1)
        # 95% C.L. conversion factor
        t1 = t.ppf(0.95, DF )
        resid = np.subtract(self.y, self.y1 )
        s_err = np.sqrt(np.sum(np.power(resid,2))/(DF))
        return t1*s_err*np.sqrt(1/len(self.x)+np.subtract(x2,np.mean(self.x))**2/np.sum(np.subtract(self.x,np.mean(self.x))**2))

    def PI(self, x2):
        DF = len(self.x)-len(self.p1)
        # 95% C.L. conversion factor
        t1 = t.ppf(0.95, DF )
        resid = np.subtract(self.y, self.y1 )
        s_err = np.sqrt(np.sum(np.power(resid,2))/(DF))

        return t1*s_err*np.sqrt(1+1/len(self.x)+(x2-np.mean(self.x))**2/np.sum((self.x-np.mean(self.x))**2))
