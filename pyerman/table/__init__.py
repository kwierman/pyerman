from pyerman.style.painters.table import TableWriter
from pyerman.style.painters import WithPainter, Paintable


@WithPainter(TableWriter)
class Table(Paintable):
    def __init__(self, headers=[], rows=[], caption=None):
        """
            Tables consist of labeled fields.
            :param headers table column headers
            :type headers list of objects with __str__ or __repr__
            :param rows iterable of row data. Row data must also be iterable
            with same length as header
            :type rows iterable

            For writing, see :class:`pyerman.style.painters.table.TableWriter`
        """
        self.headers = headers
        self.rows = rows
        self.caption = caption

    def __getitem__(self, index):
        """
            If index is of type int then retrieves row. Else retrieves column
            if header exists.
            :param index
        """
        if not type(index) == int:
            index = self.headers.index(index)
            return [row[index] for row in self.rows]
        return self.rows[index]

    def insertRow(self, row):
        if not len(row) == len(self.headers):
            msg = "Length of Row: {} is not equal to headers: {}"
            msg.format(len(row), len(self.headers))
            raise ValueError(msg)
        else:
            self.rows.append(row)

    def appendHeader(self, header, default_value='N/A'):
        self.headers.append(header)
        for row in self.rows:
            row.append(default_value)

    def sortOn(self, index=-1, header=None, reverse=False):
        if index == -1 and header is None:
            raise ValueError("Must Sort on Either Index or Header")
        elif index == -1:
            index = self.headers.index(header)
        sign = -1 if reverse else 1
        self.rows = sorted(self.rows, key=lambda x: sign*x[index])
