import ConfigParser
from . import project_directory

def default_config():
    Config = ConfigParser.ConfigParser()
    Config.read()

def get_intermediate_data_dir():
    return default_config().get("DEFAULT", "CACHEDIR")

def get_data_dir():
    return default_config().get("DEFAULT", "DATADIR")
