import time

class SaveLog:
    def __init__(self, _file_name, _now_time, _start_time, _end_time):
        self._file_name = _file_name 
        self._now_time = _now_time
        self._start_time = _start_time
        self._end_time = _end_time


class LogFile(SaveLog):

    def __init__(self, _file_name, _now_time, _start_time, _end_time):
        super().__init__(_file_name, _now_time, _start_time, _end_time)

    def save_csv(self):
        with open(self._file_name+".csv", "a") as file:
            file.write("%s, %s, %s, %s \n" %(
                                        self._now_time.now,
                                        time.strftime('%Y-%m-%d %H:%M:%s', time.gmtime(self._start_time)),
                                        time.strftime('%Y-%m-%d %H:%M:%s', time.gmtime(self._end_time)),
                                        str(self._end_time - self._start_time)))


    def save_json(self):
        with open(self._file_name, "a") as file:
            file.write("""{"now" : "%s", "start" : "%s", "end" : "%s", "time" : "%s"} \n""" %(
                                        self._now_time.now,
                                        time.strftime('%Y-%m-%d %H:%M:%s', time.gmtime(self._start_time)),
                                        time.strftime('%Y-%m-%d %H:%M:%s', time.gmtime(self._end_time)),
                                        str(self._end_time - self._start_time)))