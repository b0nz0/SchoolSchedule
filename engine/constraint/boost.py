from engine.struct import *
from db.model import DailyHour, WeekDayEnum
import json

from engine.struct import Constraint, Assignment


class Boost(Constraint):

    def __init__(self) -> None:
        super().__init__()
        self.person_id = None
        self.subject_id = None
        self.class_id = 0
        self.hour = 0
        self.day = None
        self.score = 1000
        self.weight = 1000
        self.noscore = 1

    def configure(self, person_id: int or None, subject_id: int or None, class_id: int or None,
                  day: WeekDayEnum or None, hour: int or None, score=1000):
        if subject_id:
            self.register_trigger(trigger=subject_id, trigger_type=Constraint.TRIGGER_SUBJECT)
        if person_id:
            self.register_trigger(trigger=person_id, trigger_type=Constraint.TRIGGER_PERSON)
        self.person_id = person_id
        self.subject_id = subject_id
        self.class_id = class_id
        self.hour = hour
        self.day = day
        self.score = score
        if score > 0:
            self.noscore = 0
        else:
            self.noscore = 1

    def fire(self, engine_support: EngineSupport, calendar_id: int = None, assignment: Assignment = None,
             day: WeekDayEnum = None, hour: int = None):
        assert assignment is not None, 'no assignment provided'

        subject_id = assignment.data['subject_id']
        class_id = assignment.data['class_id']
        persons = [x['person_id'] for x in assignment.data['persons']]

        if self.subject_id:
            if subject_id == self.subject_id:
                if (class_id == self.class_id or self.class_id is None) and \
                        (day == self.day or self.day is None):
                    if hour == self.hour or self.hour is None:
                        return self.score
                return self.noscore

        elif self.person_id:
            if self.person_id in persons:
                if (class_id == self.class_id or self.class_id is None) and \
                        (day == self.day or self.day is None):
                    if hour == self.hour or self.hour is None:
                        return self.score
                return self.noscore

        return 0

    def to_model(self) -> db.model.Constraint:
        constraint = self.to_model_base()
        constraint.kind = 'Boost'
        # save configuration as json string
        conf_data = dict()
        conf_data['person_id'] = self.person_id
        conf_data['subject_id'] = self.subject_id
        conf_data['class_id'] = self.class_id
        if self.day:
            conf_data['day'] = self.day.name
        else:
            conf_data['day'] = None
        conf_data['hour'] = self.hour
        constraint.configuration = json.dumps(conf_data)
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'Boost', 'returned constraint of wrong kind'
        self.from_model_base(constraint=constraint)
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
        self.configure(person_id=person_id, subject_id=subject_id, class_id=class_id, day=day, hour=hour, score=self.score)
        return self
