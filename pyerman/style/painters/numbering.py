def setNumbering(self, numbering=True):
    self.__numbering_tables__ = numbering
    self.__table_n__ = 1


class Numbered(object):
    """
        Uses numbering in data scheme
    """
    def __init__(self):
        # Nothing to do here (yet)
        pass

    def __call(self, cls):
        cls.__table_n__=1
        cls.__numbering_tables__ = False
        cls.setNumbering = setNumbering
        return cls
