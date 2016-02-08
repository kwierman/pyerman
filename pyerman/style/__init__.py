from colors import colorTable

def __repr_html__(self):
    return self.painter.__repr_html__(self)

def __repr_latex__():
    return self.painter.__repr_html__(self)

class WithPainter(object):
    def __init__(self, constructor, painter):
        self.cls = constructor
        self.painter = painter(None)
        self.cls.__repr_html__ = __repr_html__
        self.cls.__repr_latex__ = __repr_latex__
    def __call__(self, *args, **kwargs):
        print "Testing Call:"
        print args
        print kwargs
        return self.cls(args, kwargs)
