import numpy as np
from scipy.optimize import leastsq, nnls, curve_fit
from scipy.stats import norm, chisquare

def fn(acc, qU0,bmin,bmax, offset):
    E = acc+offset
    if bmin == bmax:
        return 1.e6
    elif E<qU0:
        return 0.
    elif 1.0-(bmax/bmin)*(E-qU0)/(E)<0:
        return 1.0
    elif E*(1-bmax/bmin) < qU0:
        return 1.0-np.sqrt(1.0-(bmax/bmin)*(E-qU0)/(E))
    else:
        return 1.0

def fn_list(E, qU0,bmin,bmax, offset):
    try:
        return [fn(e, qU0,bmin,bmax, offset) for e in E]
    except TypeError:
        return fn(E, qU0,bmin,bmax, offset)


def fit_fn(x,y, p0=[18575, 1, 1.e4, 18575+25], offset=0.95):
    p1, pcov = curve_fit(fn_list, x, y,p0=p0)
    x2,pvalue = chisquare(y,f_exp=[offset*fn(i,p1[0],p1[1],p1[2],p1[3]) for i in x],
                      ddof=len(p1), axis=0)
    return p1, pcov, x2, pvalue

def errf(x, a,b,c):
    return c* norm.cdf( (x-a)/b )

def fit_errf(x,y,p0=[-23.5, 0.75, 1.0]):
    p1, pcov = curve_fit(errf, x, y,p0=p0)
    x2,pvalue = chisquare(y, f_exp=[errf(i, p1[0], p1[1], p1[2]) for i in x], ddof=len(p1), axis=0)
    return p1,pcov,x2,pvalue
