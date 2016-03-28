from .base import BasicPainter
from .sanitize_for_latex import tex_escape
from numbering import Numbered

@Numbered()
class TableWriter(BasicPainter):
    def toHTML(self):
        html = ["<table width=100%>"]
        if self.host.caption is not None:
            if self._is_numbering_:
                cap = '<caption>Table {}: {}</caption>'
                cap.format(self._number_,self.host.caption)
                html.append(cap)
            else:
                html.append('<caption>{}</caption>'.format(self.host.caption))
        html.append("<tr>")
        for h in self.host.headers:
            html.append("<th>{}</th>".format(h))
        for v in self.host.rows:
            html.append("<tr>")
            for j in v: html.append("<td>{}</td>".format(j))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)

    def toLatex(self):
        out = r'\begin{table}[h]\centering\begin{tabular}{|'
        if not len(self.host.headers)==0:
            for i in self.host.headers:
              out += r'c|'
            out+=r"}\hline "
            for header in self.host.headers[:-1]:
              out += r'{} & '.format(tex_escape(header))
            out+= r'{} \\ \hline '.format(tex_escape(self.host.headers[-1]))
            for i in self.host.rows:
              for j in range(len(i)-1):
                out +=r'{} & '.format(tex_escape(i[j]))
              out+=r'{} \\ \hline '.format(tex_escape(i[len(i)-1]))
            out+=r'\end{tabular}'
        if self.host.caption is not None:
            out+=r'\caption{ '
            out+='{}'.format(tex_escape(self.host.caption))
            out+=r' }'
        out+="\end{table}"
        return out
