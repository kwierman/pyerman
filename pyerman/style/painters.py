def __repr_html__(self):
    return self.painter.toHTML(self)

def __repr_latex__(self):
    return self.painter.toLatex(self)

class Paintable(object):
    def _repr_html_(self):
        pass
    def _repr_latex_(self):
        pass
    def _repr_(self):
        pass

class BasicPainter(object):
    def toHTML(self, obj):
        return '<p color="red">Warning: Incorrect Painter Rendering: {}</p>'.format(obj)
    def toLatex(self, obj):
        return '\color{red}{Warning: Incorrect Painter Rendering: {}}'.format(obj)

class WithPainter(object):
    def __init__(self, painter):
        if painter is None:
            print("No painter argument in decorator. Call as @WithPainter(PainterClass)")
        self.painter = painter()
    def __call__(self, constructor_class):
        constructor_class.painter = self.painter
        constructor_class._repr_html_ = __repr_html__
        constructor_class._repr_latex_ = __repr_latex__
        return constructor_class
