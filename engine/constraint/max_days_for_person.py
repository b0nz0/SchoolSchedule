import db
from engine.struct import *
from db.model import DailyHour, WeekDayEnum
from engine.struct import Constraint, EngineSupport
import json


class MaximumDaysForPerson(Constraint):

    def __init__(self) -> None:
        super().__init__()
        self.person_id = None
        self.max_days = 1
        self.score = -20
        self.allowed_score = 2
        self.weight = 100
        self.register_trigger(None)

    def configure(self, person_id: int, max_days: int, score=-20):
        self.register_trigger(trigger=person_id, trigger_type=Constraint.TRIGGER_PERSON)
        self.person_id = person_id
        self.max_days = max_days
        self.score = score

    def fire(self, engine_support: EngineSupport, calendar_id: int = None, assignment: Assignment = None,
             day: WeekDayEnum = None, hour: int = None):
        assert assignment is not None, 'no assignment provided'
        assert day is not None, 'no weekday provided'
        assert hour is not None, 'no hour ordinal provided'

        # get all the persons in this assignment
        if self.person_id not in [x['person_id'] for x in assignment.data['persons']]:
            return 0

        # let's see how many days are of presence
        days_presence = set()
        for class_id in engine_support.calendars.keys():
            for day_ordinal in db.model.WeekDayEnum:
                for hour_ordinal in range(1, 11):
                    ass_in_calendar = engine_support.get_assignment_in_calendar(class_id=class_id, day=day_ordinal,
                                                                           hour_ordinal=hour_ordinal)
                    if type(ass_in_calendar) == Assignment:
                        if self.person_id in [x['person_id'] for x in ass_in_calendar.data['persons']]:
                            days_presence.add(day_ordinal)

        if day in days_presence:
            return self.allowed_score
        else:
            if len(days_presence) >= self.max_days:
                return self.score

        return 1

    def to_model(self) -> db.model.Constraint:
        constraint = self.to_model_base()
        constraint.kind = 'MaximumDaysForPerson'
        # save configuration as json string
        conf_data = dict()
        conf_data['person_id'] = self.person_id
        conf_data['max_days'] = self.max_days
        constraint.configuration = json.dumps(conf_data)
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'MaximumDaysForPerson', 'returned constraint of wrong kind'
        self.from_model_base(constraint=constraint)
        # load configuration as json string
        conf_data = json.loads(constraint.configuration)
        person_id = conf_data['person_id']
        max_days = conf_data['max_days']
        self.configure(person_id=person_id, max_days=max_days, score=self.score)
        return self
