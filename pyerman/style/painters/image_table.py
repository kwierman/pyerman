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
                html.append("<img src={}></img>".format(self.table.images[n_iter]))
                n_iter+=1
                if n_iter>=len(self.table.images):
                    break
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

    def toLatex(self, table):
        self.table = table
        out = r'\begin{table}[h]\centering\begin{tabular}{|'
        for i in self.n_cols:
            out += r'c|'
        out+=r"}\hline "

        n_iter=0
        while(n_iter<len(self.table.images)):
            for i in range(self.table.n_cols):
                out+=r'\includegraphics[width=\textwidth]{{{0}}}'.format(self.table.images[n_iter])
                n_iter+=1
                if n_iter>=len(self.table.images):
                    break
                if <self.table.n_cols-1:
                    out += r' & '
                else:
                    out+="\\"
        out+="\end{table}"
        return out
