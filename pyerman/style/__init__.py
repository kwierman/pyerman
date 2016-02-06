from colors import colorTable

def __repr_html__(self):
    return self.painter.__repr_html__()

def __repr_latex__():
    return self.painter.__repr_html__()

class WithPainter(object)
    def __init__(self, constructor, painter):
        self.cls = constructor
        self.cls.painter = painter
        self.cls.__repr_html__ = __repr_html__
        self.cls.__repr_latex__ = __repr_latex__
    def __call__(self, *args):
        return self.cls(*args)
