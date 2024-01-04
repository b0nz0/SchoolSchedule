from engine.struct import *
from db.model import DailyHour, WeekDayEnum
from engine.struct import Constraint


class NonDuplicateConstraint(Constraint):

    def __init__(self) -> None:
        super().__init__()
        self.score = -10000
        self.weight = 10000
        self.register_trigger(None)

    def fire(self, engine_support: EngineSupport, calendar_id: int = None, assignment: Assignment = None,
             day: WeekDayEnum = None, hour: int = None):
        assert assignment is not None, 'no assignment provided'
        assert day is not None, 'no weekday provided'
        assert hour is not None, 'no hour ordinal provided'

        # get all the persons in this assignment
        persons = [x['person_id'] for x in assignment.data['persons']]
        for class_id in engine_support.calendars.keys():
            ass_in_calendar = engine_support.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour)
            if ass_in_calendar == Calendar.AVAILABLE or ass_in_calendar == Calendar.UNAIVALABLE:
                continue
            # add the persons already assigned
            persons.extend([x['person_id'] for x in ass_in_calendar.data['persons']])

        # would add duplicates? in case return the score
        dup = {x for x in persons if persons.count(x) > 1}
        if len(dup) > 0:
            return self.score
        else:
            return 0

    def to_model(self) -> db.model.Constraint:
        constraint = self.to_model_base()
        constraint.kind = 'NonDuplicateConstraint'
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'NonDuplicateConstraint', 'returned constraint of wrong kind'
        self.from_model_base(constraint=constraint)
