import json

import db.model
from engine.struct import Constraint, Assignment, EngineSupport


class MaximumConsecutiveForSubject(Constraint):
    """
    boost to limit 'consecutive_hours' consecutive hours to a maximum per day
    """

    def __init__(self) -> None:
        super().__init__()
        self.subject_id = None
        self.consecutive_hours = 0
        self._suggest_continuing = False
        self.score = -10
        self.weight = 10

    def configure(self, subject_id, consecutive_hours):
        self.register_trigger(trigger=subject_id, trigger_type=Constraint.TRIGGER_SUBJECT)
        self.subject_id = subject_id
        self.consecutive_hours = consecutive_hours

    def fire(self, engine_support: EngineSupport, calendar_id: int = None, assignment: Assignment = None,
             day: db.model.WeekDayEnum = None, hour: int = None):
        assert assignment is not None, 'no assignment provided'
        assert calendar_id is not None, 'no calendar provided'
        assert day is not None, 'no weekday provided'
        assert hour is not None, 'no hour ordinal provided'

        self._suggest_continuing = False
        if assignment.data['subject_id'] != self.subject_id:
            return 0

        # let's see if a max-1 assignment have been done in past/future
        tot = 0
        for i in range(hour-self.consecutive_hours, hour):
            ass_m = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=i)
            if type(ass_m) == Assignment and ass_m.data['subject_id'] == self.subject_id:
                tot += 1
        for i in range(hour+1, hour+self.consecutive_hours+1):
            ass_m = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=i)
            if type(ass_m) == Assignment and ass_m.data['subject_id'] == self.subject_id:
                tot += 1
        if tot >= self.consecutive_hours:
            return self.score
        else:
            return 0

    def suggest_continuing(self):
        return self._suggest_continuing

    def to_model(self) -> db.model.Constraint:
        constraint = self.to_model_base()
        constraint.kind = 'MaximumConsecutiveForSubject'
        # save configuration as json string
        conf_data = dict()
        conf_data['subject_id'] = self.subject_id
        conf_data['consecutive_hours'] = self.consecutive_hours
        constraint.configuration = json.dumps(conf_data)
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'MaximumConsecutiveForSubject', 'returned constraint of wrong kind'
        self.from_model_base(constraint=constraint)
        # load configuration as json string
        conf_data = json.loads(constraint.configuration)
        subject_id = conf_data['subject_id']
        consecutive_hours = conf_data['consecutive_hours']
        self.configure(subject_id=subject_id, consecutive_hours=consecutive_hours)
