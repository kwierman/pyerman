from .base import BasicPainter
from .numbering import Numbered
from .sanitize_for_latex import tex_escape

@Numbered()
class ImageTablePainter(BasicPainter):

    def toHTML(self, table):
        self.table = table
        html = ["<table width=100%>"]
        if self.table.caption is not None:
            if self.__numbering_tables__:
                html.append('<caption>Table {}: {}</caption>'.format(self.__table_n__,self.table.caption))
            else:
                html.append('<caption>{}</caption>'.format(self.table.caption))
        n_iter=0
        while(n_iter<len(self.table.images)):
            html.append("<tr>")
            for i in range(self.table.n_cols):
                html.append('<td><img src={} ></img></td>'.format(self.table.images[n_iter]))
                n_iter+=1
                if n_iter>=len(self.table.images):
                    break
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

    def toLatex(self, table):
        self.host = table
        out = r'\begin{table}[h]\centering\begin{tabular}{|'
        if not self.host.n_cols==0:
            for i in range(self.host.n_cols):
              out += r'c|'
            out+=r"}\hline "
            current_col=0
            for image in self.host.images:
                if current_col == self.host.n_cols-1:
                    out+= r'{} \\ \hline '.format(r'\adjustimage{{max size={{{0}\textwidth}}{{{0}\paperheight}}}}{{{1}}}'.format(1.0/self.host.n_cols, image))
                    current_col=0
                else:
                    out+= r'{} & '.format(r'\adjustimage{{max size={{{0}\textwidth}}{{{0}\paperheight}}}}{{{1}}}'.format(1.0/self.host.n_cols, image))
                    current_col +=1
            out+=r'\end{tabular}'
        if self.host.caption is not None:
            out+=r'\caption{ '
            out+='{}'.format(tex_escape(self.host.caption))
            out+=r' }'
        out+="\end{table}"
        return out
