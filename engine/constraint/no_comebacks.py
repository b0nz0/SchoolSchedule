import db
from engine.struct import *
from db.model import DailyHour, WeekDayEnum
from engine.struct import Constraint


class NoComebacks(Constraint):

    def __init__(self) -> None:
        super().__init__()
        self.score = -10
        self.weight = 20
        self.register_trigger(None)

    def fire(self, engine_support: EngineSupport, calendar_id: int = None, assignment: Assignment = None,
             day: WeekDayEnum = None, hour: int = None):
        assert calendar_id is not None, 'no calendar provided'
        assert assignment is not None, 'no assignment provided'
        assert day is not None, 'no weekday provided'
        assert hour is not None, 'no hour ordinal provided'

        # get all the persons in this assignment
        persons = [x['person_id'] for x in assignment.data['persons']]

        # cycle thru the hours before this one in the same day
        for currhour in [x for x in range(1, 11) if x < hour - 1 or x > hour + 1]:
            ass_in_calendar = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day,
                                                                        hour_ordinal=currhour)
            if ass_in_calendar == Calendar.AVAILABLE or ass_in_calendar == Calendar.UNAIVALABLE:
                continue
            # would add duplicates? in case return the score
            for person_id in [x['person_id'] for x in ass_in_calendar.data['persons']]:
                if person_id in persons:
                    return self.score

        return 0

    def to_model(self) -> db.model.Constraint:
        constraint = self.to_model_base()
        constraint.kind = 'NoComebacks'
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'NoComebacks', 'returned constraint of wrong kind'
        self.from_model_base(constraint=constraint)
