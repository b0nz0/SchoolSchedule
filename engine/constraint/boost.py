from engine.struct import *
from db.model import DailyHour, WeekDayEnum
import json

class Boost(Constraint):
    
    def __init__(self) -> None:
        super().__init__()
        self._subject_id = None
        self._class_id = 0
        self._hour = 0
        self._day = None
        self.score = 1000
        self.weight = 1000

    def configure(self, subject_id: int, class_id: int, day: WeekDayEnum, hour: int, score=1000):
        self.register_trigger(trigger=subject_id, trigger_type=Constraint.TRIGGER_SUBJECT)
        self._subject_id = subject_id
        self._class_id = class_id
        self._hour = hour
        self._day = day
        self.score = score
        
    def fire(self, engine_support: EngineSupport, calendar_id:int=None, assignment:Assignment=None, day:WeekDayEnum=None, hour:int=None):
        assert assignment != None, 'no assignment provided'
        assert day != None, 'no weekday provided'
        assert hour != None, 'no hour ordinal provided'

        subject_id = assignment.data['subject_id']
        class_id = assignment.data['class_id']
        if subject_id == self._subject_id and \
                (class_id == self._class_id or self._class_id == None) and \
                (day == self._day or self._day == None):
             if hour == self._hour:
                return self.score
             elif hour == self._hour - 1:
                return 0-self.score
             elif hour == self._hour + 1:
                return 0-self.score
             else: 
                return 0
        else:
            return 0

    def to_model(self) -> db.model.Constraint:
        constraint = db.model.Constraint()
        constraint.identifier = self.identifier
        constraint.kind = 'Boost'
        # save configuration as json string
        conf_data = dict()
        conf_data['subject_id'] = self._subject_id
        conf_data['class_id'] = self._class_id
        conf_data['day'] = self._day
        conf_data['hour'] = self._hour
        conf_data['score'] = self.score
        constraint.configuration = json.dumps(conf_data)
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'Boost', 'returned constraint of wrong kind'
        self.identifier = constraint.identifier
        # load configuration as json string
        conf_data = json.loads(constraint.configuration)
        subject_id = conf_data['subject_id']
        class_id = conf_data['class_id']
        day = conf_data['day']
        hour = conf_data['hour']
        score = conf_data['score']
        self.configure(subject_id=subject_id, class_id=class_id, day=day, hour=hour, score=score)
        return self
