from pyerman.files import Config
from exceptions import ValueError

class LSFConfig(Config):
    def __init__(self,username=None, password=None, server=None, section='default'):
        """
            LSFConfig() #Gets the default config
            LSFConfig(default_server)
            LSFConfig(username, password, server)
        """
        Config.__init__(self, config_filename='.lsf.cfg', section=section)
        if server is None:
            self.server = self['server']
        else:
            self.server = server
            self['server'] = server
        if username is None or password is None:
            try:
                self.username = self['username']
                self.password = self['password']
            except ValueError:
                message="""No username and password found on record
                Please run LSFConfig("username","password","server")
                To establish a defined default configuration
                """
                raise ValueError(message)
        else:
            self['username'] = username
            self['password'] = password
            self.username = username
            self.password = password

__lsfConfigSingleton__ = None
def getLSFConfigSingleton(username=None, password=None, default_server=None):
    if __lsfConfigSingleton__ is None:
        __lsfConfigSingleton__ = LSFConfig(username, password, default_server)
    return __lsfConfigSingleton__
