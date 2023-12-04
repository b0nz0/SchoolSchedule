import db.query
import db.model

class Assignment:
    _id = 0
    _subject_in_class_id = 0
    _data = {}
    _score = 0
    
    def __init__(self, id) -> None:
        self._id = id
        self._subject_in_class_id = 0
        self._data = dict()
        self._score = 0
    
    
    def as_copy(self, from_assignment):
        self._subject_in_class_id = from_assignment.subject_in_class_id
        self._classe = from_assignment.class_.copy()
        self._subject = from_assignment.subject.copy()
        self._persons = from_assignment.persons[:]
        self._room = from_assignment.room.copy()
        self._score = 0
            
    @property
    def id(self):
        return self._id
    
    @property
    def subject_in_class_id(self):
        return self._subject_in_class_id

    @subject_in_class_id.setter
    def subject_in_class_id(self, subject_in_class_id):
        self._subject_in_class_id = subject_in_class_id
    
    @property
    def data(self):
        return self._data
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, score):
        self._score = score
        
class Calendar:
    _id = 0
    _days = {}
    
    UNAIVALABLE = -1
    AVAILABLE = 0
    
    def __init__(self, id=None) -> None:
        if id:
            self._id = id
        else:
            self._id = 0
        self._days = {}
        
    def load(self, plan_id: int):
        if len(self._days.keys) > 0:
            print(f'Calendario {self._id} già caricato. Sovrascrivo\n')
        plan = db.query.get_plan(plan_id)
        if plan:
                for day in plan.keys():
                    self._days[day] = {}
                    for hour in plan[day]:
                        self._days[day][hour.ordinal] = Calendar.AVAILABLE
        else:
            print(f'Plan ID {plan_id} non trovato\n')
            
    def day(self, day_id):
        if day_id in self._days.keys():
            return self._days[day_id]
        else:
            return None
        
class EngineSupport(object):
    _calendars = []
    _assignments = {}
    _constraints = []

    def __init__(self) -> None:
        self._calendars = {}
        self._assignments = {}
        self._constraints = []
  
    def get_assignment(self, assignment_id = None) -> Assignment:
        if assignment_id in self._assignments.keys():
            return self._assignments[assignment_id]  
        if not assignment_id:    
            assignment_id = len(self._assignments.keys())
            self._assignments[assignment_id] = Assignment(id=assignment_id)
            return self._assignments[assignment_id]      
        if assignment_id not in self._assignments.keys:
            return None
    
    def load_assignments_from_subject_in_class(self, subject_in_class_id: int):
        sic = db.query.get(db.model.SubjectInClass, id=subject_in_class_id)
        if sic:
            for p in sic.persons:
                assignment = self.get_assignment()
                assignment.subject_in_class_id = subject_in_class_id
                assignment.data['class_id'] = sic.class_id
                assignment.data['section'] = sic.class_.section.identifier
                assignment.data['year']= sic.class_.year.identifier
                assignment.data['subject_id']= sic.subject.id
                assignment.data['subject'] = sic.subject.identifier
                assignment.data['person_id'] = p.id
                assignment.data['person'] = p.fullname
                assignment.data['room_id'] = sic.room.id
                assignment.data['room'] = sic.room.identifier
                assignment.score = 0
    
    def get_calendar(self, calendar_id = None) -> Calendar:
        if calendar_id in self._calendars.keys():
            return self._calendars[calendar_id]  
        if not calendar_id:    
            calendar_id = len(self._calendars.keys())
        if calendar_id not in self._calendars.keys:
            self._calendars[calendar_id] = Calendar(id=calendar_id)
        return self._calendars[calendar_id]      

    def get_assignment_in_calendar(self, calendar_id, day, hour_ordinal):
        calendar = self.get_calendar(calendar_id=calendar_id)
        plan_day = calendar.day(day_id=day)
        if plan_day:
            if hour_ordinal in plan_day:
                return plan_day[hour_ordinal]
            else:
                return Calendar.UNAIVALABLE    
        else:
            return Calendar.UNAIVALABLE
        
    def get_calendar_ids(self):
        return self._calendars.keys()
    
    @property
    def constraints(self):
        return self._constraints
    
