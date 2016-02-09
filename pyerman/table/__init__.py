from pyerman.style.table import TableWriter
from pyerman.style import WithPainter, Paintable

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

    def insert_row(self, row):
        if not len(row) == len(self.headers):
            raise ValueError("Length of Row: {} is not equal to headers: {}".format(len(row), len(self.headers)))
        else:
            self.rows.append(row)

    def append_header(self, header, default_value='N/A'):
        self.headers.append(header)
        for row in rows:
            row.append(default_value)
