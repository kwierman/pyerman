import ConfigParser
import collections
import os

class Config(collections.MutableMapping):
    __here__ = os.getcwd()
    def __init__(self, config_filename='.pyerman.cfg', section='defaults'):
        self.config = ConfigParser.ConfigParser()
        self.section = section
        self.filename = os.path.join(self.getConfigDir(), config_filename)
        self.read()

    def __del__(self):
        self.write()

    def read(self):
        self.store={}
        try:
            with open(self.filename,'r') as input_config:
                self.config.readfp(input_config)
                options = self.config.options(self.section)
                for option in options:
                    try:
                        self.store[option] = self.config.get(self.section, option)
                    except:
                        print("exception on %s!" % option)
                        self.store[option] = None
        except IOError:
            print("Config Does Not Exist. Creating new file {} ".format(self.filename))
            self.write()

    def write(self):
        with open(self.filename,'w') as input_config:
            for key, value in self.store:
                self.config.set(self.section, key, value)
            self.config.write(input_config)


    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    @classmethod
    def _getDefaultDir(cls, dirname):
        full_path = os.path.join(cls.__here__, dirname)
        if not os.path.isdir(full_path):
            os.mkdir(full_path)
        return full_path

    @classmethod
    def getConfigDir(cls):
        return cls._getDefaultDir('config')

    @classmethod
    def getDataDir(cls):
        return cls._getDefaultDir('data')

    @classmethod
    def getPlotDir(cls):
        return cls._getDefaultDir('plots')

    @classmethod
    def getScriptDir(cls):
        return cls._getDefaultDir('scripts')
