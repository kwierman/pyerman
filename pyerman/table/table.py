from pyerman.style.table import TableWriter
from pyerman.style import WithPainter

@WithPainter(TableWriter)
class Table(object):
    def __init__(self, *args, **kwargs):
        """
            Tables consist of labeled fields.
            :param headers table column headers
            :type headers list of objects with __str__ or __repr__
            :param rows iterable of row data. Row data must also be iterable
            with same length as header
            :type rows iterable
        """
        self.headers = []
        if 'headers' in kwargs:
            self.headers = kwargs['headers']
        self.rows = []
        if 'rows' in kwargs:
            self.rows = kwargs['rows']
        self.caption = None
        if 'caption' in kwargs:
            self.caption = kwargs['caption']

    def __getitem__(self, index):
        """
            If index is of type int then retrieves row. Else retrieves column
            if header exists.
            :param index
        """
        if not type(index) == int:
            index = self.headers.index(index)
            return [row[index] for row in self.rows]
        return rows[index]

    def insert_row(self, row):
        if not len(row) == len(self.headers):
            raise ValueError("Length of Row: {} is not equal to headers: {}".format(len(row), len(headers)))
        else:
            self.rows.append(row)

    def append_header(self, header, default_value='N/A'):
        self.headers.append(header)
        for row in rows:
            row.append(default_value)
