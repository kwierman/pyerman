import numpy

def compute_residuals(x1,x2,y1,y2,y1_err,y2_err):
    y=[]
    y_err=[]
    x=[]
    x_err=[]
    
    for index1 in range(len(x1)):
        x2min = min(x2, key=lambda x: abs(x1[index1] - x) )
        index2= x2.index(x2min)
        if abs(x1[index1]-x2[index2]) > 2:
            continue
        
        
        y.append( y2[index2]-y1[index1]  )
        err = numpy.sqrt( (y1_err[index1]**2)+(y2_err[index2]**2))
        if not y2[index2]-y1[index1]:
            err=0
        else:
            err /=(y2[index2]-y1[index1])
        y_err.append( err )
        x.append( (x1[index1]+x2[index2])/2.0 )
        x_err.append( abs(x1[index1]-x2[index2])/2.0 )
    
    return x,y,x_err,y_err

def simple_residual_cut(x,y,xerr,yerr, threshold=100.0):
    out = {'x':[],'y':[],'xerr':[],'yerr':[]}
    for i in range(1, len(y)):
        diff = abs(y[i]-y[i-1])
        if  diff <= threshold :
            out['x'].append(x[i])
            out['y'].append(y[i])
            out['xerr'].append(xerr[i])
            out['yerr'].append(yerr[i])
    return out