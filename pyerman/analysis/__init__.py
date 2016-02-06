#!/usr/bin/python



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
