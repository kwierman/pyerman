def _setNumbering(self, numbering=True):
    self._is_numbering_ = numbering
    self._number_ = 1


class Numbered(object):
    """
        Uses numbering in data scheme
    """
    def __init__(self, numbering=True):
        self._is_numbering_ = numbering
        self._number_ = 0

    @property
    def number(self):
        self._number_ += 1
        return self._number_

    def __call__(self, host):
        host.setNumbering = _setNumbering
        host.counter = self
        return host
