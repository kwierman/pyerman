#!/usr/bin/python
from scipy.optimize import leastsq, nnls, curve_fit
from scipy.stats import norm, chisquare
import numpy
import math

def skew(x,args):
    t = numpy.divide(numpy.subtract(x,args[0]) , args[1] )
    return numpy.multiply(args[3], numpy.multiply( (2.0), numpy.multiply( norm.pdf(t), norm.cdf( numpy.multiply(args[2],t) ) ) ) )

def skew_with_params(x, e=0.0,w=1.0,a=1.0,amp=1.0,off=0.0):
    t = (x-e)/w
    return off+amp*(2.0)*norm.pdf(t)*norm.cdf(a*t ) 

def gaus(x, args):
    return  args[2] * norm.pdf( (x-args[0] )/args[1] )

def errf(x, args):
    return args[2]* norm.cdf( (x-args[0])/args[1] )

def errf_with_params(x, a,b,c):
    return a* norm.cdf( (x-b)/c )

def line(x, args):
    return numpy.add(numpy.multiply(args[0],x) , args[1] )


class KJW_fitter(object):

    def __init__(self, func = gaus, p0=[0.0,1.0,1.0,0.0] ):
        self.func = func
        self.p0= p0

    def least_squares(self, x,y):
        fitfunc = lambda p, x: self.func(x,p ) # Target function
        errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
        errfuncSquare = lambda p, x, y: (fitfunc(p, x) - y)**2.0
        p1,pcov,infodict,mesg, success = leastsq(errfunc, self.p0[:], args=(x, y), full_output=True)
        #print p1, pcov, infodict, mesg, success
        #popt, pcov = curve_fit(skew, x, y,p0)
        #print "Optimal Values for: ", config['dipole'],":",popt
        #print pcov
        self.p1 = p1
        self.pcov = pcov
        fit_error_sum = sum(errfuncSquare(p1, x[:len(x)/2],y[:len(x)/2]  ) )
        fit_error_sum /=float(len(x))
        self.fit_error = numpy.sqrt(  fit_error_sum )

    def getparError(self, i):
    	perr = numpy.sqrt(numpy.diag(self.pcov))
    	return self.pcov[i][i]*perr
        #now to get estimates on the errors of the values

    def non_negative_least_squares(self, A,b):
    	return nnls(A,b)

    def curve_fit(self, x,y, y_err=None):
        #This is a hack
        fitfunc = lambda p, x: self.func(x, p[0]) # Target function
        if(len(self.p0)==2):
        	fitfunc = lambda p, x: self.func(x, p[0],p[1]) # Target function
        elif(len(self.p0)==3):
        	fitfunc = lambda p, x: self.func(x, p[0],p[1],p[2]) # Target function
        elif(len(self.p0)==4):
        	fitfunc = lambda p, x: self.func(x, p[0],p[1],p[2],p[3]) # Target function
        elif(len(self.p0)==5):
        	fitfunc = lambda p, x: self.func(x, p[0],p[1],p[2],p[3],p[4]) # Target function
        elif(len(self.p0)==6):
        	fitfunc = lambda p, x: self.func(x, p[0],p[1],p[2],p[3],p[4],p[5]) # Target function
            
        errfunc = lambda p, x, y: fitfunc(p, x) - y
        errfuncSquare = lambda p, x, y: (fitfunc(p, x) - y)**2.0
        
        self.p1, self.pcov = curve_fit(self.func, x, y,p0=self.p0)
        
        self.confidence_interval=[]
        error_ranges=[ numpy.linspace(self.p1[i]+self.getparerror(i), self.p1[i]-self.getparerror(i),3) for i in range(len(self.p0) ) ]

        for i in x:
            x_values=[]
            for j in error_ranges[0]:
                for k in error_ranges[1]:
                    for l in error_ranges[2]:
                        for m in error_ranges[3]:
                            for n in error_ranges[4]:
                                clfunc = lambda p, x: self.func(x, p[0],p[1],p[2],p[3],p[4])
                                p2 = [j,k,l,m,n]
                                x_values.append( clfunc(p2,i) )
            #now find the values that contain 95% of all values
            x_values = sorted(x_values)
            n_in_cl = float(len(x_values))*0.05
            m_in = x_values[int(n_in_cl/2) ]
            m_ax = x_values[int(len(x_values)-n_in_cl/2) ]
            self.confidence_interval.append([m_in,m_ax])
        
        #fit_error_sum = sum(errfuncSquare(self.p1, x[:len(x)/2],y[:len(x)/2]  ) )
        #fit_error_sum /=float(len(x))
        #self.fit_error = numpy.sqrt(  fit_error_sum )
        
        self.chisquare,self.pvalue = chisquare(y, f_exp=[fitfunc(self.p1, i) for i in x], ddof=len(self.p0), axis=0)
        #self.chisquare=0
        #for i,j in enumerate(x):
        #    self.chisquare+=( fitfunc(self.p1,j)-y[i] )**2/(self.confidence_interval[i][1]-self.confidence_interval[i][0])**2

    def getparerror(self, i):
        return numpy.sqrt(numpy.diag(self.pcov))[i]

    def getChiSquared(self):
      	return abs(self.chisquare)
        #return scipy.stats.chisquare(f_obs, f_exp=None, ddof=0, axis=0)[source]
        

        
        
class CurveFitter(object):

    def __init__(self, func = gaus, p0=[0.0,1.0,1.0,0.0] ):
        self.func = func
        self.p0= p0
        self.error_resolution= 3 #sigma


    def getparError(self, i):
    	perr = numpy.sqrt(numpy.diag(self.pcov))
    	return self.pcov[i][i]*perr
        #now to get estimates on the errors of the values

    def non_negative_least_squares(self, A,b):
    	return nnls(A,b)
    
    def _gen_recursive_errors(self, set_params, params):
        output = []
        if len(params)==1:
            return []
        return output
            

    def curve_fit(self, x,y, y_err=None):
                    
        self.p1, self.pcov = curve_fit(self.func, x, y,p0=[self.p0])
        """
        self.confidence_interval=[]
        #now generate out the 
        
        
        error_ranges=[numpy.linspace(self.p1[i]+self.getparError(i), self.p1[i]-self.getpErerror(i),self.error_resolution) for i in range(len(self.p0) ) ]
        permutations = 
        #generate out all the permutations
            
        

        for i in x:
            x_values=[]
            for j in error_ranges[0]:
                for k in error_ranges[1]:
                    for l in error_ranges[2]:
                        for m in error_ranges[3]:
                            for n in error_ranges[4]:
                                clfunc = lambda p, x: self.func(x, p[0],p[1],p[2],p[3],p[4])
                                p2 = [j,k,l,m,n]
                                x_values.append( clfunc(p2,i) )
            #now find the values that contain 95% of all values
            x_values = sorted(x_values)
            n_in_cl = float(len(x_values))*0.05
            m_in = x_values[int(n_in_cl/2) ]
            m_ax = x_values[int(len(x_values)-n_in_cl/2) ]
            self.confidence_interval.append([m_in,m_ax])
        
        
        #fit_error_sum = sum(errfuncSquare(self.p1, x[:len(x)/2],y[:len(x)/2]  ) )
        #fit_error_sum /=float(len(x))
        #self.fit_error = numpy.sqrt(  fit_error_sum )
        
        #self.chisquare,self.pvalue = chisquare(y, f_exp=[fitfunc(self.p1, i) for i in x], ddof=len(self.p0), axis=0)
        #self.chisquare=0
        #for i,j in enumerate(x):
        #    self.chisquare+=( fitfunc(self.p1,j)-y[i] )**2/(self.confidence_interval[i][1]-self.confidence_interval[i][0])**2

    def getparerror(self, i):
        return numpy.sqrt(numpy.diag(self.pcov))[i]

    def getChiSquared(self):
      	return abs(self.chisquare)
        #return scipy.stats.chisquare(f_obs, f_exp=None, ddof=0, axis=0)[source]
        """

        