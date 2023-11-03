class Base:

    _object_id = 0
    _start_date = None
    _end_date = None
    _active = True
    _log_user = None

    @property
    def object_id(self):
        return self._object_id
    
    @object_id.setter
    def object_id(self, object_id):
        self._object_id = object_id

    @property
    def start_date(self):
        return self._start_date
    
    @start_date.setter
    def start_date(self, start_date):
        self._start_date = start_date

    @property
    def end_date(self):
        return self._end_date
    
    @end_date.setter
    def end_date(self, end_date):
        self._end_date = end_date

    @property
    def active(self):
        return self._active
    
    @active.setter
    def end_date(self, active):
        self._active = active

    @property
    def log_user(self):
        return self._log_user
    
    @log_user.setter
    def log_user(self, log_user):
        self._log_user = log_user

    def __init__(self) -> None:
        _id = 0
        _start_date = None
        _end_date = None
        _active = True
        _log_user = None

class School(Base):
    def __init__(self) -> None:
        super(School, self).__init__()

    
        
