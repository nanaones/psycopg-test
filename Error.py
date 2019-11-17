import pytz

class ABErrorClass(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class DBSaveError(ABErrorClass):
    def __init__(self, msg="Use pg_query series only."):
        self.msg = msg

    def __str__(self):
        super.__str__()

class TimeZoneError(ABErrorClass):
    def __init__(self, msg="Plz check timezone."):
        self.msg = msg

    def __str__(self):
        return self.msg

class LogFileFormatError(ABErrorClass):
    def __init__(self, msg="Plz check logfileformat ('_log_type')"):
        self.msg = msg

    def __str__(self):
        return self.msg
