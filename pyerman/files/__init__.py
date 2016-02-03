import os

__here__ = os.getcwd()
__default_dirs__ = ["config","data","plots","scripts"]


def setup():
    for d in __default_dirs__:
        full_path = os.path.join(__here__, __default_dirs__)
        if not os.path.isdir(full_path):
            os.mkdir(full_path)
