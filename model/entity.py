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

    
        
class SchoolYear(Base):

    _identifier = None
    _school = None

    def __init__(self) -> None:
        super(SchoolYear, self).__init__()

    @property
    def identifier(self):
        return self._identifier
    
    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def school(self):
        return self._school
    
    @school.setter
    def school(self, school:School):
        self._school = school

class Year(Base):

    _identifier = None
    _school = None

    def __init__(self) -> None:
        super(Year, self).__init__()

    @property
    def identifier(self):
        return self._identifier
    
    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def school(self):
        return self._school
    
    @school.setter
    def school(self, school:School):
        self._school = school

class Section(Base):

    _identifier = None
    _school = None

    def __init__(self) -> None:
        super(Section, self).__init__()

    @property
    def identifier(self):
        return self._identifier
    
    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def school(self):
        return self._school
    
    @school.setter
    def school(self, school:School):
        self._school = school

class Class(Base):
    _schoolYear = None
    _year = None
    _section = None

    def __init__(self) -> None:
        super(Class, self).__init__()

    @property
    def schoolYear(self):
        return self._schoolYear
    
    @schoolYear.setter
    def schoolYear(self, schoolYear:SchoolYear):
        self._schoolYear = schoolYear

    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, year:Year):
        self._year = year

    @property
    def section(self):
        return self._section
    
    @section.setter
    def section(self, section:Section):
        self._section = section

