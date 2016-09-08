import numpy as np
from itertools import islice

def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

class GaussianValue:
    """
        Calculation of mean and st dev from iterable values and propogates these
        values through operators

        :note
        Error Propogation Values are copied from: (here)[https://en.wikipedia.org/wiki/Propagation_of_uncertainty]
    """
    def __init__(self, iterable=None, val=None, error=None):
        self.iterable = iterable
        if iterable is not None:
            self.val = np.average(iterable)
            self.err = np.std(iterable)
        else:
            if val is None and error is None:
                raise ValueError("Gaussian Value Cannot be initialized with all None Values")
            self.val = val
            self.err = error


    def __repr__(self):
        return u"{:.2g} +/- {:.2g}".format(self.val, self.err)

    def __str__(self):
        return str(self.__repr__())

    def __add__(self, other):
        """
            $$
                \sigma = \sqrt(\sigma_A^2+\sigma_b^2+2cov(AB))
            $$
        """
        val = self.val+other.val
        err=0.0
        if self.iterable and other.iterable:
            cov = np.cov(self.iterable, other.iterable)
            err = np.sqrt(np.power(cov[0][0],2)+np.power(cov[1][1],2)+cov[0][1]+cov[1][0])
        else:
            err = np.sqrt(np.power(self.err,2)+np.power(other.err, 2))
        return GaussianValue(None, val, err)


    def __sub__(self, other):
        """
            $$
                \sigmas = \sqrt(\sigma_A^2+\sigma_B^2-2cov(AB))
            $$
        """
        val = self.val-other.val
        err=0.0
        if self.iterable and other.iterable:
            cov = np.cov(self.iterable, other.iterable)
            err = np.sqrt(np.power(cov[0][0],2)+np.power(cov[1][1],2)-cov[0][1]-cov[1][0])
        else:
            err = np.sqrt(np.power(self.err,2)+np.power(other.err, 2))
        return GaussianValue(None, val, err)


    def __mul__(self, other):
        """
            $$
                \sigmas = \sqrt(B^2\sigma_A^2+A^2\sigma_B^2+2ABcov(AB))
            $$
        """
        val = self.val*other.val
        err=0.0
        if self.iterable and other.iterable:
            cov = np.cov(self.iterable, other.iterable)
            err = np.power(other.val*cov[0][0],2)+np.power(self.val*cov[1][1],2)
            err-= self.val*other.val*(cov[0][1]+cov[1][0])
            err = np.sqrt(err)
        else:
            err = np.sqrt(np.power(self.err*other.val,2)+np.power(other.err*self.val, 2))
        return GaussianValue(None, val, err)

    def __div__(self, other):
        """
            $$
                \sigmas = \sqrt(\sigma_A^2/A^2+\sigma_B^2/B^2+2ABcov(AB))
            $$
        """
        val = self.val/other.val
        err=0.0
        if self.iterable and other.iterable:
            cov = np.cov(self.iterable, other.iterable)
            err = np.power(cov[0][0]/self.val,2)+np.power(cov[1][1]/other.val,2)
            err-= (cov[0][1]+cov[1][0])/(self.val*other.val)
            err = np.sqrt(err)
        else:
            err = np.sqrt(np.power(self.err/self.val,2)+np.power(other.err/other.val, 2))
        return GaussianValue(None, val, err)
