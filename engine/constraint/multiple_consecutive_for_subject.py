from engine.struct import Calendar, Constraint, Assignment, EngineSupport
import db.model 
import json

class MultipleConsecutiveForSubject(Constraint):
    
    def __init__(self) -> None:
        super().__init__()
        self._subject_id = None
        self._consecutive_hours = 0
        self._times = 1
        self._suggest_continuing = False
        self.score = 10
        self.weight = 10

    def configure(self, subject_id, consecutive_hours, times=1):
        self.register_trigger(trigger=subject_id, trigger_type=Constraint.TRIGGER_SUBJECT)
        self._subject_id = subject_id
        self._consecutive_hours = consecutive_hours
        self._times = times
        
    def fire(self, engine_support: EngineSupport, calendar_id:int=None, assignment:Assignment=None, day:db.model.WeekDayEnum=None, hour:int=None):
        assert assignment != None, 'no assignment provided'
        assert calendar_id != None, 'no calendar provided'
        assert day != None, 'no weekday provided'
        assert hour != None, 'no hour ordinal provided'

        self._suggest_continuing = False
        if assignment.data['subject_id'] != self._subject_id:
            return 0
        
        # let's see if a multiple day is already present
        ntimes = 0
        for day_ordinal in db.model.WeekDayEnum:
            nfound = 0
            for hour_ordinal in range(1, 11):  
                assignment = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day_ordinal, hour_ordinal=hour_ordinal)
                if type(assignment) == Assignment:
                    if assignment.data['subject_id'] == self._subject_id:
                        nfound = nfound + 1
            if nfound >= self._consecutive_hours:
                ntimes = ntimes + 1
                
        # no previous assignments that satisfy the constraint
        if ntimes < self._times:
            self._suggest_continuing = False
            ass_m1 = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=hour-1)
            if type(ass_m1) == Assignment and ass_m1.data['subject_id'] == self._subject_id: 
                return self.score*10
            ass_p1 = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=hour+1)
            if type(ass_p1) == Assignment and ass_p1.data['subject_id'] == self._subject_id: 
                return self.score*10
            self._suggest_continuing = True
            return self.score
        else:
            self._suggest_continuing = False
            return 0

    def suggest_continuing(self):
        return self._suggest_continuing

    def to_model(self) -> db.model.Constraint:
        constraint = db.model.Constraint()
        constraint.identifier = self.identifier
        constraint.kind = 'MultipleConsecutiveForSubject'
        # save configuration as json string
        conf_data = dict()
        conf_data['subject_id'] = self._subject_id
        conf_data['consecutive_hours'] = self._consecutive_hours
        conf_data['times'] = self._times
        constraint.configuration = json.dumps(conf_data)
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'MultipleConsecutiveForSubject', 'returned constraint of wrong kind'
        self.identifier = constraint.identifier
        # load configuration as json string
        conf_data = json.loads(constraint.configuration)
        subject_id = conf_data['subject_id']
        consecutive_hours = conf_data['consecutive_hours']
        times = conf_data['times']
        self.configure(subject_id=subject_id, consecutive_hours=consecutive_hours, times=times)

'''    
        ntimes = 0
        for day_ordinal in db.model.WeekDayEnum:
            nfound = 0
            for hour_ordinal in range(1, 11):  
                assignment = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day_ordinal, hour_ordinal=hour_ordinal)
                if type(assignment) == Assignment:
                    if assignment.data['subject_id'] == self._subject_id:
                        nfound = nfound + 1
            if nfound >= self._consecutive_hours:
                ntimes = ntimes + 1
        if ntimes < self._times and \
            engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=hour+1) == Calendar.AVAILABLE:
            self._suggest_continuing = True
            return self.score
        else:
            self._suggest_continuing = False
            return 0
'''
