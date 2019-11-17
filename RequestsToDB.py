import json
from configparser import ConfigParser
import os


class RequestsToDB:
    
    def __init__(self, _configpath='./config/config.ini'):        
        if not os.getenv("CONFIGPATH") is None:
            _configpath = os.getenv("CONFIGPATH")
            
        self.config_data = self._config(path=_configpath)     

    def _config(self, _configParser=ConfigParser, path='', _print=False):
        """
        add path & add configparser obj it will print sections and values in config file
        
        :param _configParser: ConfigPartser Class / path = the path where config.ini file exist
        :return: configparser Object 
        
        """
        _config = _configParser()
        _config.read(path)
        _section = _config.sections()
        if _print:
            for _ in _section:
                print(f"section = {_}")
                for options in _config[_]:
                    _data = _config.get(_, options)
                    print(f"{options} = {_data}")
                    
        return _config
            
