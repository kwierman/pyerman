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
        self.table = table
        out = r'\begin{table}[h]\centering\begin{tabular}{|'
        for i in range(self.table.n_cols):
            out += r'c|'
        out+=r"}\hline "

        n_iter=0
        while(n_iter<len(self.table.images)):
            for i in range(self.table.n_cols):
                out+=r' \includegraphics[width={0}\textwidth]{{{1}}} '.format(float(1./self.table.n_cols),self.table.images[n_iter])
                n_iter+=1
                if n_iter>=len(self.table.images):
                    break
                if n_iter<self.table.n_cols:
                    out += r' & '
                else:
                    out+=r'{} \\ \hline '
        if self.table.caption is not None:
            out+=r'\caption{ '
            out+=r'{}'.format(tex_escape(self.table.caption))
            out+=r' }'
        out+=r"\end{table}"
        print out
        return out
