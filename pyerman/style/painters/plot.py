from .painters import BasicPainter
import matplotlib.pyplot as plt
from pyerman.style import colorTable
from pyerman.style.displayables import KJWImageTable

class PlotPainter(BasicPainter):

    def paint(self, obj):
        plt.errorbar( obj.x,obj.y,xerr=obj.xerr, yerr=obj.yerr,color=colorTable(0), fmt='o')
    def toHTML(self, obj):
        plt.figure()
        self.paint(obj)
        plt.title(obj.title)
        plt.xlabel(obj.xaxis_title)
        plt.ylabel(obj.yaxis_title)
        plt.grid(True)
        plt.show()

    def toLatex(self, obj):
        plt.figure()
        self.paint(obj)
        plt.title(obj.title)
        plt.xlabel(obj.xaxis_title)
        plt.ylabel(obj.yaxis_title)
        plt.grid(True)
        plt.savefig("plots/bp_trans.pdf" )
        plt.savefig("plots/bp_trans.svg" )
        plt.clf()
        plt.close(fig)
        plt.close('all')
        KJWImageTable(["plots/bp_trans"])
