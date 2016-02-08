# Sets the table numbering
__table_n__=1
__numbering_tables__ = False


class TableWriter:
    def __init__(self, table):
        self.table = table
    def setNumbering(self, numbering=True):
        global __numbering_tables__
        __numbering_tables__ = numbering
        global __table_n__
        __table_n__ = 1

    def _repr_html_(self):
        global __table_n__
        global __numbering_tables__
        html = ["<table width=100%>"]
        if self.table.caption is not None:
            if __numbering_tables__:
                html.append('<caption>Table {}: {}</caption>'.format(__table_n__,self.caption))
            else:
                html.append('<caption>{}</caption>'.format(self.caption))
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

    def _repr_latex_(self):
        global __table_n__
        global __numbering_tables__
        out = r'\begin{table}[h]\centering\begin{tabular}{|'
        for i in self.table.headers:
          out += r'c|'
        out+=r"}\hline "
        for header in self.table.headers[:-1]:
          out += r'{} & '.format(header)
        out+= r'{} \\ \hline '.format(self.table.headers[-1])

        for i in self.table.rows:
          for j in range(len(i)-1):
            out +=r'{} & '.format(i[j])
          out+=r'{} \\ \hline '.format(i[len(i)-1])
        out+=r'\end{tabular}'
        if self.table.caption is not None:
            out+=r'\caption{ '
            if __numbering_tables__:
                out+=r'Table {}: '.format(__table_n__)
                __table_n__+=1
            out+='{}'.format(self.table.caption)
            out+=r' }'
        out+="\end{table}"
        return out
