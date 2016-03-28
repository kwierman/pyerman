def _setNumbering(self, numbering=True):
    self.__numbering_tables__ = numbering
    self.__table_n__ = 1


class Numbered(object):
    """
        Uses numbering in data scheme
    """
    def __call__(self, cls):
        global _setNumbering
        cls.__table_n__=1
        cls.__numbering_tables__ = False
        cls.setNumbering = _setNumbering
        return cls
