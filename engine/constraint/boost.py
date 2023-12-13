from engine.struct import *
from db.model import DailyHour, WeekDayEnum
import json

class Boost(Constraint):
    
    def __init__(self) -> None:
        super().__init__()
        self._person_id = None
        self._subject_id = None
        self._class_id = 0
        self._hour = 0
        self._day = None
        self.score = 1000
        self.weight = 1000
        self.noscore = 1

    def configure(self, person_id: int, subject_id: int, class_id: int, day: WeekDayEnum, hour: int, score=1000):
        if subject_id:
            self.register_trigger(trigger=subject_id, trigger_type=Constraint.TRIGGER_SUBJECT)
        if person_id:
            self.register_trigger(trigger=person_id, trigger_type=Constraint.TRIGGER_PERSON)
        self._person_id = person_id
        self._subject_id = subject_id
        self._class_id = class_id
        self._hour = hour
        self._day = day
        self.score = score
        if score > 0: self.noscore = 0
        else: self.noscore = 1
        
    def fire(self, engine_support: EngineSupport, calendar_id:int=None, assignment:Assignment=None, day:WeekDayEnum=None, hour:int=None):
        assert assignment != None, 'no assignment provided'

        subject_id = assignment.data['subject_id']
        class_id = assignment.data['class_id']
        persons = [x['person_id'] for x in assignment.data['persons']]
        
        if self._subject_id:
            if subject_id == self._subject_id:
                if  (class_id == self._class_id or self._class_id == None) and \
                    (day == self._day or self._day == None):
                    if hour == self._hour or self._hour == None:
                        return self.score
                return self.noscore
            
        elif self._person_id:
            if self._person_id in persons:
                if (class_id == self._class_id or self._class_id == None) and \
                    (day == self._day or self._day == None):
                    if hour == self._hour or self._hour == None:
                        return self.score
                return self.noscore

        return 0
    
    def to_model(self) -> db.model.Constraint:
        constraint = db.model.Constraint()
        constraint.identifier = self.identifier
        constraint.kind = 'Boost'
        # save configuration as json string
        conf_data = dict()
        conf_data['person_id'] = self._person_id
        conf_data['subject_id'] = self._subject_id
        conf_data['class_id'] = self._class_id
        if self._day:
            conf_data['day'] = self._day.name
        else:
            conf_data['day'] = None
        conf_data['hour'] = self._hour
        conf_data['score'] = self.score
        constraint.configuration = json.dumps(conf_data)
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'Boost', 'returned constraint of wrong kind'
        self.identifier = constraint.identifier
        # load configuration as json string
        conf_data = json.loads(constraint.configuration)
        person_id = conf_data['person_id']
        subject_id = conf_data['subject_id']
        class_id = conf_data['class_id']
        loadday = conf_data['day']
        if loadday:
            for wd in WeekDayEnum:
                if loadday == wd.name:
                    day = wd
        else:
            day = None
        hour = conf_data['hour']
        score = conf_data['score']
        self.configure(person_id=person_id, subject_id=subject_id, class_id=class_id, day=day, hour=hour, score=score)
        return self
