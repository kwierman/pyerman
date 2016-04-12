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
        html.append("<tr>")
        for h in self.table.headers:
            html.append("<th>{}</th>".format(h))
        for v in self.table.rows:
            html.append("<tr>")
            for j in v:
                html.append("<td>{}</td>".format(j))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

    def toLatex(self, table):
        self.table = table
        out = r'\begin{table}[h]\centering\begin{tabular}{|'
        if not len(self.table.headers)==0:
            for i in self.table.headers:
              out += r'c|'
            out+=r"}\hline "
            for header in self.table.headers[:-1]:
              out += r'{} & '.format(tex_escape(header))
            out+= r'{} \\ \hline '.format(tex_escape(self.table.headers[-1]))
            for i in self.table.rows:
              for j in range(len(i)-1):
                out +=r'{} & '.format(tex_escape(i[j]))
              out+=r'{} \\ \hline '.format(tex_escape(i[len(i)-1]))
            out+=r'\end{tabular}'
        if self.table.caption is not None:
            out+=r'\caption{ '
            out+='{}'.format(tex_escape(self.table.caption))
            out+=r' }'
        out+="\end{table}"
        return out
