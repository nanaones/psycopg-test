from RequestsToDB import RequestsToDB
from DB import pg_query, pg_query_pool
import Decorator

import time
import sys

class MainClass:

    def __init__(self, _loop=100):
        self._loop = _loop
        self.query = RequestsToDB().config_data.get("SQL", 
                                                    "INSERT")
        self.log_save_path = RequestsToDB().config_data.get("LOG", 
                                                    "logSavePath")
        self.log_save = RequestsToDB().config_data.getboolean("LOG", 
                                                    "logSave")
        self.log_type = RequestsToDB().config_data.get("LOG", 
                                                    "logType")
        
    @Decorator.time_print
    def loop_query_pool(self, _message="pool", _thread="single"):
        for _num in range(self._loop):
            pg_query_pool(_query=str(self.query).replace("?", 
                                                         f"'{_message} - {str(_num)}'"),
                                                         _save = self.log_save, 
                                                         _log_save_folder_path=self.log_save_path,
                                                         _log_type=self.log_type,
                                                         _thread=_thread)        

    @Decorator.time_print
    def loop_query(self, _message="basic"):
        for _num in range(self._loop):
            pg_query(_query=str(self.query).replace("?", 
                                                    f"'{_message} - {str(_num)}'"),
                                                         _save = self.log_save, 
                                                         _log_save_folder_path=self.log_save_path,        
                                                         _log_type=self.log_type)        


if __name__ == "__main__":
    main = MainClass(_loop=int(sys.argv[1]))
    main.loop_query_pool(_thread="single")
    main.loop_query_pool(_thread="multi")
    main.loop_query()
    