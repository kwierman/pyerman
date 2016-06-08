from pyerman.style.painters import Paintable, WithPainter
from pyerman.style.painters.image_table import ImageTablePainter

@WithPainter(ImageTablePainter)
class ImageTable(Paintable):
    """
        Basic Table for painting images in tabulated form
    """
    def __init__(self, images=[], n_cols = 2, caption=None):
        self.images=images
        self.n_cols=n_cols
        self.caption = caption

    def __getitem__(self, index):
        """
            If index is of type int then retrieves row. Else retrieves column
            if header exists.
            :param index
        """
        return self.images[index]
