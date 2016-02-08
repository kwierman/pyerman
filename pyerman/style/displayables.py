import os

class PDF(object):
  def __init__(self, pdf, size=(200,200)):
    self.pdf = pdf
    self.size = size

  def _repr_html_(self):
    return '<iframe src={0} width={1[0]} height={1[1]}></iframe>'.format(self.pdf, self.size)

  def _repr_latex_(self):
    return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(self.pdf)


class SVGTable:
    def __init__(self, names):
        self.names=names
    def _repr_html_(self):
        html = ["<table width=100%>"]
        n_col=2
        l = len(self.names)
        if l>8:
            n_col=4

        html.append("<tr>")
        j=0
        for i in self.names:
            html.append('<td><img src="{}" width="100%" alt="Nice green circle"/></td>'.format(i))
            j+=1
            if(j==n_col):
                html.append("</tr>")
                j=0
        for i in range(n_col-j):
            html.append("<td></td>")
        if not j==n_col:
            html.append("</tr>")
        return ''.join(html)
    def _repr_latex_(self):
      out=r'\begin{tabular}{cc}'
      j=0
      for i in self.names:
        #out+=SVG(i)._repr_svg_()
        if j ==1:
          out+= r' & '
        else:
          out+= r' // '
      out+=r'\end{tabular}'
      return out

class KJWImageTable:
    def __init__(self, names, usepng=False):
        self.curdir = os.getcwd()
        self.names=names
        self.usepng = usepng
    def _repr_html_(self):
        html = ["<table width=100%>"]
        n_col=2 if len(self.names)>1 else 1
        l = len(self.names)
        if l>8:
            n_col=4

        html.append("<tr>")
        j=0
        for i in self.names:
            if self.usepng:
                html.append('<td><img src="{}.png" width="100%" alt="Image Rendering or Not Found"/></td>'.format(i))
            else:
                html.append('<td><img src="{}.svg" width="100%" alt="Image Rendering or Not Found"/></td>'.format(i))
            j+=1
            if(j==n_col):
                html.append("</tr>")
                j=0
        if not j==0:
          for i in range(n_col-j):
              html.append("<td></td>")
        if not j==n_col:
            html.append("</tr>")
        return ''.join(html)

    def _repr_latex_(self):

      out=r'\begin{tabular}{|c|c|} \hline'
      if (len(self.names)==1):
            out=r''
      j=1
      for i in self.names:
        if len(self.names)==1:
            out+=r'\includegraphics[width=\textwidth]{{{0}/{1}.pdf}}'.format(self.curdir,i)
        else:
            out+=r'\includegraphics[width=0.5\textwidth]{{{0}/{1}.pdf}}'.format(self.curdir,i)
        if (len(self.names)==1):
          continue
        if j ==1:
          out+= r' & '
          j = 0
        else:
          out+= r' \\ \hline '
          j = 1
      if not len(self.names)==1:
          out+=r'\end{tabular}'
      return out
