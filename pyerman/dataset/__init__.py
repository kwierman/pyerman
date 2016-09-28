import numpy
from scipy import stats


class Bin(object):
    def __init__(self, edge, value=[]):
        self.edge = edge
        self.value = value


class BinContainer(object):
    def __init__(self, lo=0, hi=1.e6, nbins=1000):
        self.z_map = []
        for i in numpy.linspace(lo, hi, nbins):
            self.z_map.append(Bin(i, []))

    def insert(self, edge, value):
        for index, bin_ in enumerate(self.z_map):
            if edge >= bin_.edge and edge < self.z_map[index+1].edge:
                bin_.value.append(value)
                return

    def calc_stats(self):
        dat = {}
        for i in self.z_map:
            if len(i.value) > 0:
                ave = numpy.average(i.value)
                err = numpy.std(i.value)
                dat[i.edge] = (ave, err)
        return dat
