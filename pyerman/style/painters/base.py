def __repr_html__(self):
    return self.painter.toHTML()

def __repr_latex__(self):
    return self.painter.toLatex()


class BasicPainter(object):
    def toHTML(self):
        return '<p color="red">Warning: Incorrect Painter Rendering</p>'
    def toLatex(self):
        return '\color{red}{Warning: Incorrect Painter Rendering'


class WithPainter(object):
    def __init__(self, painter):
        if painter is None:
            print("No painter argument in decorator. Call as @WithPainter(PainterClass)")
        self.painter = painter()
    def __call__(self, host):
        host.painter = self.painter
        self.painter.host = host
        host._repr_html_ = __repr_html__
        host._repr_latex_ = __repr_latex__
        return host
