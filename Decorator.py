import time
import datetime

import Error
from CustomTime import CustomTime
from RequestsToDB import RequestsToDB
from LogFIle import LogFile

def time_print(function):
    def func(*args):
        
        _start_time = time.time()
        print(f"[start]{function.__name__}")
        function(*args)
        _end_time = time.time()
        print(f"[result][{function.__name__}] {_end_time - _start_time} (sec)")
        print(f"[end]{function.__name__}")

    return func

# Only Use 'pg_query*'
def save_resp_time(function):
    def func(
            _log_type="json",
            _save=False, 
            _log_save_folder_path='./', 
            _functions_name=["pg_query", "pg_query_pool"],
            *args,  
            **kwargs):

        _now_time = CustomTime(_time_zone=RequestsToDB().config_data.get("TIME", "timeZone"))
        if _save:
            _function_name = function.__name__
            _file_name = f"{_log_save_folder_path}{_function_name}-{ str(_now_time.now).split(' ')[0]}"
            if _function_name in _functions_name:
                _start_time = time.time()
                function(*args, **kwargs)
                _end_time = time.time()
                _log_file = LogFile(
                        _file_name=_file_name,
                        _now_time=_now_time, 
                        _start_time=_start_time,
                        _end_time=_end_time)

                if _log_type == "json":
                    _log_file.save_json()
                elif _log_type == "csv":
                    _log_file.save_csv()
                else:
                    raise Error.LogFileFormatError()
            else:
                raise Error.DBSaveError()
        else: 
            pass
    return func

