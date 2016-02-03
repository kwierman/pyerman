#!/usr/bin/python


default_configuration = =[{'dipole':4.0, 'up':23408, 'down':23409, 'chaos':23411},
             {'dipole':3.5, 'up':23403, 'down':23404, 'chaos':23406},
             {'dipole':3.0, 'up':23393, 'down':23398, 'chaos':23400},
             {'dipole':2.5, 'up':23414, 'down':23415, 'chaos':23421},
             {'dipole':0.5, 'up':24104, 'down':24105, 'chaos':24107},
             {'dipole':0.1, 'up':24110, 'down':24108, 'chaos':24111}]

class AnalysisConfiguration(object):
    def __init__(self, config = default_configuration):
        selfs.config = config

class DataSet(object):
    def __init__(self, x,y,xerr,yerr):
        self.x = x
        self.y = y
        self.xerr = xerr
        self.yerr=yerr
    def __init__(self, other):
        self.x = other.x
        self.y=other.y
        self.xerr=other.xerr
        self.yerr=other.yerr
    def __init(self, config):
        self.x = config['X']
        self.y = config['Y']
        self.xerr = config['ERR_X']
        self.yerr = config['ERR_Y']
        
        
class DrawDataSet(DataSet):
    def __init__(self,x,y,xerr,yerr):
        super(self).__init__(x,y,xerr,yerr)
        
    def draw(self, color=0, name="something"):
        pass
    def show(self):
        pass

class DataSetReverser(DataSet):
    def __init__(self,x,y,xerr,yerr):
        super(self).__init__(x,y,xerr,yerr)
        self.y = [ i for i in reversed(self.y)]
        self.yerr =[i for i in reversed(self.yerr) ]

class CombinedDataSets(object):
    def __init__(self, up,down):
        self.up=up
        self.down=down
        
class ThresholdMatcher(CombinedDataSets):
    def __init__(self, up, down):
        super(self).__init__(up,down)
    def compute(self, threshold=150):
        first_index=0
        second_index =0

        for i in range(1,len(self.up.y)):
            if self.up.y[i]-self.up.y[i-1]>threshold:
                first_index=i
                break
        for i in range(1,len(self.ydown)):
            if self.down.y[i]-self.down.y[i-1]>threshold:
                second_index=i
                break
        diff = abs(first_index-second_index)
        if(second_index<first_index):
            self.down.x = [i+diff for i in self.down.x ]
            self.down.xerr = [ i for i in self.down.xerr ]
        else:
            self.up.x    = [i+diff for i in self.up.x ]
            self.up.xerr = [i for i in self.up.xerr ]
        return first_index, second_index
        
class Residual(CombinedDataSets):
    def __init__(self, up, down):
        self.up = up
        self.down=down

    def compute(self):
        y=[]
        y_err=[]
        x=[]
        x_err=[]
        for index1 in range(len(self.up.x)):
            x2min = min(self.down.x, key=lambda x: abs(self.up.x[index1] - x) )
            index2= self.down.x.index(x2min)
            
            y.append( self.down.y[index2]-self.up.y[index1]  )
            err = numpy.sqrt( (self.up.yerr[index1]**2)+(self.down.yerr[index2]**2))
            if not self.down.yerr[index2]-self.up.yerr[index1]:
                err=0
            else:
                err /=(self.down.yerr[index2]-self.up.yerr[index1])
            y_err.append( err )
            x.append( (self.down.x[index1]+self.up.x[index2])/2.0 )
            x_err.append( abs(self.up.x[index1]-self.down.x[index2])/2.0 )
    
    return x,y,x_err,y_err



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

def line(x, args):
    return numpy.add(numpy.multiply(args[0],x) , args[1] )


class KJW_fitter(object):

    def __init__(self, func = gaus, p0=[0.0,1.0,1.0] ):
        self.func = func
        self.p0= p0

    def least_squares(self, x,y):
        fitfunc = lambda p, x: self.func(x,self.p0 ) # Target function
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
                        clfunc = lambda p, x: self.func(x, p[0],p[1],p[2],p[3])
                        for m in error_ranges[3]:
                            p2 = [j,k,l,m]
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
        
