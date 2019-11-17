import time
import datetime

import Error
from CustomTime import CustomTime
from RequestsToDB import RequestsToDB

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
    def func(*args, _save=False, _log_save_folder_path='./', _functions_name=["pg_query", "pg_query_pool"], **kwargs):
        if _save:
            _function_name = function.__name__
            _file_name = f"{_log_save_folder_path}{_function_name}{ str(datetime.datetime.now()).split(' ')[0]}"
            # if ((_function_name == "pg_query") or (_function_name == "pg_query_pool")): 
            if _function_name in _functions_name:
                _start_time = time.time()
                function(*args, **kwargs)
                _end_time = time.time()
                _now_time = CustomTime(_time_zone=RequestsToDB().config_data.get("TIME", "timeZone"))

                with open(_file_name, "a") as file:
                    file.write("%s, %s, %s, %s \n" %(
                                                _now_time.now,
                                                time.strftime('%Y-%m-%d %H:%M:%s', time.gmtime(_start_time)),
                                                time.strftime('%Y-%m-%d %H:%M:%s', time.gmtime(_end_time)),
                                                str(_end_time -_start_time)))
            else:
                raise Error.DBSaveError()

    return func


# def _save_csv():
# def _save_json():
    