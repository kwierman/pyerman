class Table(object):
    def __init__(self, headers=[], rows=[]):
        self.headers = headers
        self.rows = rows
        self.caption = None
    def __getitem__(self, header):
        index = self.headers.index(header)
        return [row[index] for row in self.rows]
    def insert_row(self, row):
        if not len(row) == len(self.headers):
            raise ValueError("Length of Row: {} is not equal to headers: {}".format(len(row), len(headers)))
        else:
            self.rows.append(row)
    def append_header(self, header, default_value=0.0):
        self.headers.append(header)
        for row in rows:
            row.append(default_value)
    def _repr_html_(self):
        html = ["<table width=100%>"]
        if self.caption is not None:
            html.append('<caption>{}</caption>'.format(self.caption))
        html.append("<tr>")
        for h in self.headers:
            html.append("<th>{}</th>".format(h))
        for v in self.rows:
            html.append("<tr>")
            for j in v:
                html.append("<td>{}</td>".format(j))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)
    def _repr_latex_(self):
      out = r'\begin{table}[h]\centering\begin{tabular}{|'
      for i in self.headers:
        out += r'c|'
      out+=r"}\hline "
      for header in self.headers[:-1]:
        out += r'{} & '.format(header)
      out+= r'{} \\ \hline '.format(self.headers[-1])

      for i in self.rows:
        for j in range(len(i)-1):
          out +=r'{} & '.format(i[j])
        out+=r'{} \\ \hline '.format(i[len(i)-1])
        #out.append(r' // /hline')
      out+=r'\end{tabular}'
      if self.caption is not None:
          out+=r'\caption{ ' +str(self.caption)+ r' }'
      out+="\end{table}"
      return out
