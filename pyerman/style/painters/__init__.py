from .base import BasicPainter, WithPainter
from .numbering import Numbered

class Paintable(object):
    def _repr_html_(self):
        pass
    def _repr_latex_(self):
        pass
    def _repr_(self):
        pass
