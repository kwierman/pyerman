from pyerman.style.painters.plot import PlotPainter
from pyerman.style.painters import WithPainter, Paintable

import copy

class PlotItem():
    """
        Mixin for items that are meant to be plotted.
    """
    def __init__(self, x=[],y=[],xerr=[],yerr=[]):
        self.x = x
        self.y = y
        self.xerr = xerr
        self.yerr=yerr
    def __init__(self, other=None):
        if other is None:
            PlotItem.__init__(self)
        self.x = copy.copy(other.x)
        self.y = copy.copy(other.y)
        self.xerr = copy.copy(other.xerr)
        self.yerr = copy.copy(other.yerr)



@WithPainter(PlotPainter)
class Plot(Paintable):
    pass
