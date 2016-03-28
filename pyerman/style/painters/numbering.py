def _setNumbering(self, numbering=True):
    self._is_numbering_ = numbering
    self._number_ = 1


class Numbered(object):
    """
        Uses numbering in data scheme
    """
    def __call__(self, host):
        host._number_=1
        host._is_numbering_ = False
        host.setNumbering = _setNumbering
        return host
