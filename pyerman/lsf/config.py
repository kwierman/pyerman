from pyerman.files import Config
from exceptions import ValueError

class LSFConfig(Config):
    def __init__(self,username=None, password=None, default_server=None):
        #if the default server is none, then
        if default_server is None:
            Config.__init__(self, config_filename='.lsf.cfg', section='default')
            if self.username is None and self.password is None:
                if not 'username' in self or 'password' in self or 'server' in self:
                    message="""No username and password found on record
                    Please run LSFConfig("username","password","server")
                    To establish a defined default configuration
                    """
                    raise ValueError(message)

            else:
                self['username'] = username
                self['password'] = password
                self['default_server'] = default_server

__lsfConfigSingleton__ = None
def getLSFConfigSingleton(username=None, password=None, default_server=None):
    if __lsfConfigSingleton__ is None:
        __lsfConfigSingleton__ = LSFConfig(username, password, default_server)
    return __lsfConfigSingleton__
