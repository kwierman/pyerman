import copy
from pyerman.style import WithPainter, Paintable
from pyerman.style.dataset import DatasetPainter

@WithPainter(DatasetPainter)
class DataSet(Paintable):
    def __init__(self, x=[],y=[],xerr=[],yerr=[]):
        self.x = x
        self.y = y
        self.xerr = xerr
        self.yerr=yerr
    def __init__(self, other=None):
        if other is None:
            DataSet.__init__(self)
        self.x = copy.copy(other.x)
        self.y = copy.copy(other.y)
        self.xerr = copy.copy(other.xerr)
        self.yerr = copy.copy(other.yerr)
    def __init__(self, config):
        self.x = config['X']
        self.y = config['Y']
        self.xerr = config['ERR_X']
        self.yerr = config['ERR_Y']


import numpy
from scipy import stats
class Bin(object):
    def __init__(self, edge, value=[]):
        self.edge=edge
        self.value = value

class BinContainer(object):
    def __init__(self, lo=0, hi=1.e6, nbins=1000):
        self.z_map=[]
        for i in numpy.linspace(lo,hi,nbins):
            self.z_map.append(Bin(i,[]))
    def insert(self, edge, value):
        for index, bin_ in enumerate(self.z_map):
            if edge>=bin_.edge and edge<self.z_map[index+1].edge:
                bin_.value.append(value)
                return
    def calc_stats(self):
        dat={}
        for i in self.z_map:
            if len(i.value)>0:
                ave = numpy.average(i.value)
                err = numpy.std(i.value)
                dat[i.edge]=(ave,err)
        return dat
