import matplotlib.pyplot as plt
from pyerman.files.config import Config

__current_dataset_number__ = 0

class DatasetPainter:
    def __init__(self, dataset):
        self.dataset= dataset

    def createPlot(self):
        pass
    def _repr_html_(self):
        #create the plot
        #save the plot
        #return the SVG or PDF of the plot
        pass
    def _repr_latex_(self):
        #create the plot
        #save the plot
        #return the SVG or PDF of the plot
        pass
