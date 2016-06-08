import matplotlib.pyplot as plt
from .painters import BasicPainter
#from pyerman.files.config import Config

__current_dataset_number__ = 0

class DatasetPainter(BasicPainter):
    def __init__(self, dataset=None):
        global __current_dataset_number__

        if dataset is None:
            print("No Dataset handed to painter")
        self.dataset= dataset
        self.datasetnumber = __current_dataset_number__
        __current_dataset_number__+=1
