from RequestsToDB import RequestsToDB
from DB import pg_query, pg_query_pool
import Decorator

import time
import sys

class MainClass:

    def __init__(self, _loop=100, minconn=1, _log_save_folder_path="/logs/", _log_type="json"):
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
    def loop_query_pool_single(self, _message="pool", _thread="single", _save = True ,_log_save_folder_path="/logs/", _log_type="json"):
        for _num in range(self._loop):
            pg_query_pool(_query=str(self.query).\
                        replace("?", f"'{_message*10} - {str(_num)}'"),
                        _save = _save, 
                        _log_save_folder_path=_log_save_folder_path,
                        _log_type=self.log_type,
                        _thread=_thread,
                        _printing=False,
                        minconn=1)

    @Decorator.time_print
    def loop_query_pool(self, _message="pool", _thread="single", minconn=1, _save = True ,_log_save_folder_path="/logs/", _log_type="json"):
        _query=[str(self.query).replace("?", f"'{_message*10} - {str(_num)}'")  for _num in range(self._loop)]
        pg_query_pool(_query=_query,
                        _save = _save, 
                        _log_save_folder_path=_log_save_folder_path,
                        _log_type=_log_type,
                        _thread=_thread,
                        _printing=False,
                        minconn=1)

    @Decorator.time_print
    def loop_query(self, _message="basic", _save = True ,_log_save_folder_path="/logs/", _log_type="json"):
        for _num in range(self._loop):
            pg_query(_query=str(self.query).replace("?", 
                                                    f"'{_message*10} - {str(_num)}'"),
                                                         _save = _save, 
                                                         _log_save_folder_path=_log_save_folder_path,        
                                                         _log_type=_log_type)

if __name__ == "__main__":
    _loop = int(sys.argv[1])
    minconn = int(sys.argv[2])
    _log_save_folder_path = str(sys.argv[3])
    _log_type = str(sys.argv[4])

    main = MainClass(_loop=_loop)
    main.loop_query_pool_single(_thread="single", _log_save_folder_path=_log_save_folder_path, _log_type=_log_type)
    main.loop_query_pool(_thread="multi", minconn=minconn, _log_save_folder_path=_log_save_folder_path, _log_type=_log_type)
    main.loop_query(_log_save_folder_path=_log_save_folder_path, _log_type=_log_type)
