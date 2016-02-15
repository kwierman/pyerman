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
    def __init__(self, other):
        self.x = copy.copy(other.x)
        self.y = copy.copy(other.y)
        self.xerr = copy.copy(other.xerr)
        self.yerr = copy.copy(other.yerr)
    def __init__(self, config):
        self.x = config['X']
        self.y = config['Y']
        self.xerr = config['ERR_X']
        self.yerr = config['ERR_Y']
