def __repr_html__(self):
    return self.painter.toHTML(self)

def __repr_latex__(self):
    return self.painter.toLatex(self)


class BasicPainter:
    def toHTML(self, obj):
        return '<p color="red">Warning: Incorrect Painter Rendering</p>'
    def toLatex(self, obj):
        return '\color{red}{Warning: Incorrect Painter Rendering'


class WithPainter:
    def __init__(self, painter):
        if painter is None:
            print("No painter argument in decorator. Call as @WithPainter(PainterClass)")
        self.painter = painter()
    def __call__(self, host):
        host.painter = self.painter
        host._repr_html_ = __repr_html__
        host._repr_latex_ = __repr_latex__
        return host
