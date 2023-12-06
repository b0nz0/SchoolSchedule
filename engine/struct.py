import db.query
import db.model

class Assignment:

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
    
    UNAIVALABLE = -1
    AVAILABLE = 0
    
    def __init__(self, id=None) -> None:
        if id:
            self._id = id
        else:
            self._id = 0
        self._days = {}
        
    def load(self, plan_id: int):
        if len(self._days.keys()) > 0:
            print(f'Calendario {self._id} già caricato. Sovrascrivo\n')
        plan = db.query.get_plan(plan_id)
        if plan:
            for day in plan.keys():
                self._days[day] = {}
                for daily_hour in plan[day]:
                    self._days[day][daily_hour.ordinal] = Calendar.AVAILABLE
        else:
            print(f'Plan ID {plan_id} non trovato\n')
            
    def day(self, day_id):
        if day_id in self._days.keys():
            return self._days[day_id]
        else:
            return None
        
class EngineSupport(object):

    def __init__(self) -> None:
        self._calendars = {}
        self._assignments = {}
        self._constraints = []
        self._persons = {}
  
    def get_assignment(self, subject_in_class_id: int):
        if subject_in_class_id in self._assignments.keys():
            return self._assignments[subject_in_class_id]  
        else:
            self._assignments[subject_in_class_id] = Assignment(id=subject_in_class_id)
            return self._assignments[subject_in_class_id]
    
    def load_assignment_from_subject_in_class(self, subject_in_class_id: int):
        sic = db.query.get(db.model.SubjectInClass, id=subject_in_class_id)
        if sic:
            assignment = self.get_assignment(subject_in_class_id=subject_in_class_id)
            assignment.subject_in_class_id = subject_in_class_id
            assignment.data['class_id'] = sic.class_id
            assignment.data['section'] = sic.class_.section.identifier
            assignment.data['year']= sic.class_.year.identifier
            assignment.data['subject_id']= sic.subject.id
            assignment.data['subject'] = sic.subject.identifier
            assignment.data['persons'] = []
            # add all persons to the assignment
            for p in sic.persons:
                d = dict()
                d['person_id'] = p.id
                d['person'] = p.fullname
                assignment.data['persons'].append(list(d))
                # link the identifier to each person, for later use
                if p.id not in self._persons.keys():
                    self._persons[p.id] = []
                self._persons[p.id].append(subject_in_class_id)
            assignment.data['room_id'] = sic.room.id
            assignment.data['room'] = sic.room.identifier
            assignment.score = 0
            assignment.data['calendar'] = self.get_calendar(sic.class_id)
                
    def get_calendar(self, class_id = None) -> Calendar:
        if class_id in self._calendars.keys():
            return self._calendars[class_id]  
        else: 
            plan_id = db.query.get_plan_for_class(class_id)
            if plan_id:    
                self._calendars[class_id] = Calendar(id=class_id)
                self._calendars[class_id].load(plan_id=plan_id)  
                return self._calendars[class_id]    

    def get_assignment_in_calendar(self, class_id, day, hour_ordinal):
        calendar = self.get_calendar(class_id=class_id)
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
    
