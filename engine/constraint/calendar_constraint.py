import db
from engine.struct import *
from db.model import DailyHour, WeekDayEnum
from engine.struct import Constraint, EngineSupport
import json


class CalendarDays(Constraint):

    def __init__(self) -> None:
        super().__init__()
        self.person_id = None
        self.allowed_hours_list = list()
        self.score = -100
        self.allowed_score = 1
        self.weight = 100
        self.register_trigger(None)

    def configure(self, person_id: int, allowed_hours_list, score=-100):
        self.register_trigger(trigger=person_id, trigger_type=Constraint.TRIGGER_PERSON)
        self.person_id = person_id
        self.allowed_hours_list = allowed_hours_list
        self.score = score

    def fire(self, engine_support: EngineSupport, calendar_id: int = None, assignment: Assignment = None,
             day: WeekDayEnum = None, hour: int = None):
        assert assignment is not None, 'no assignment provided'
        assert day is not None, 'no weekday provided'
        assert hour is not None, 'no hour ordinal provided'

        # get all the persons in this assignment
        if self.person_id not in [x['person_id'] for x in assignment.data['persons']]:
            return 0

        for (allowed_day, allowed_hour) in self.allowed_hours_list:
            if allowed_day == day and allowed_hour == hour:
                return self.allowed_score

        # no allowed match
        return self.score

    def to_model(self) -> db.model.Constraint:
        constraint = self.to_model_base()
        constraint.kind = 'CalendarDays'
        # save configuration as json string
        conf_data = dict()
        conf_data['person_id'] = self.person_id
        conf_data['allowed_hours_list'] = [(k.value, v) for (k, v) in self.allowed_hours_list]
        constraint.configuration = json.dumps(conf_data)
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'CalendarDays', 'returned constraint of wrong kind'
        self.from_model_base(constraint=constraint)
        # load configuration as json string
        conf_data = json.loads(constraint.configuration)
        person_id = conf_data['person_id']
        allowed_hours_list = list()
        for (k, v) in conf_data['allowed_hours_list']:
            for day in WeekDayEnum:
                if day.value == k:
                    allowed_hours_list.append((day, v))
        self.configure(person_id=person_id, allowed_hours_list=allowed_hours_list, score=self.score)
        return self
