from engine.struct import Calendar, Constraint, Assignment, EngineSupport
import db.model
import json


class MultipleConsecutiveForSubject(Constraint):
    ''' 
    boost 'consecutive_hours' consecutive hours, given that it has not been already assigned at least 'times' times.
    no boost if current hour > 4, because this constraint is targeted at early hours
    '''

    def __init__(self) -> None:
        super().__init__()
        self.subject_id = None
        self.consecutive_hours = 0
        self.times = 1
        self._suggest_continuing = False
        self.score = 10
        self.weight = 10

    def configure(self, subject_id, consecutive_hours, times=1):
        self.register_trigger(trigger=subject_id, trigger_type=Constraint.TRIGGER_SUBJECT)
        self.subject_id = subject_id
        self.consecutive_hours = consecutive_hours
        self.times = times

    def fire(self, engine_support: EngineSupport, calendar_id: int = None, assignment: Assignment = None,
             day: db.model.WeekDayEnum = None, hour: int = None):
        assert assignment is not None, 'no assignment provided'
        assert calendar_id is not None, 'no calendar provided'
        assert day is not None, 'no weekday provided'
        assert hour is not None, 'no hour ordinal provided'

        self._suggest_continuing = False
        if assignment.data['subject_id'] != self.subject_id:
            return 0

        # let's see if a multiple day is already present
        ntimes = 0
        for day_ordinal in db.model.WeekDayEnum:
            nfound = 0
            for hour_ordinal in range(1, 11):
                assignment = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day_ordinal,
                                                                       hour_ordinal=hour_ordinal)
                if type(assignment) == Assignment:
                    if assignment.data['subject_id'] == self.subject_id:
                        nfound = nfound + 1
            if nfound >= self.consecutive_hours:
                ntimes = ntimes + 1

        # no previous assignments that satisfy the constraint
        if ntimes < self.times:
            self._suggest_continuing = False
            ass_m1 = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=hour - 1)
            if type(ass_m1) == Assignment and ass_m1.data['subject_id'] == self.subject_id:
                return self.score * 10
            ass_p1 = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=hour + 1)
            if type(ass_p1) == Assignment and ass_p1.data['subject_id'] == self.subject_id and hour < 5:
                return self.score * 10
            if hour < 5:
                self._suggest_continuing = True
                return self.score
            else: 
                return 0
        else:
            self._suggest_continuing = False
            return 0

    def suggest_continuing(self):
        return self._suggest_continuing

    def to_model(self) -> db.model.Constraint:
        constraint = self.to_model_base()
        constraint.kind = 'MultipleConsecutiveForSubject'
        # save configuration as json string
        conf_data = dict()
        conf_data['subject_id'] = self.subject_id
        conf_data['consecutive_hours'] = self.consecutive_hours
        conf_data['times'] = self.times
        constraint.configuration = json.dumps(conf_data)
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'MultipleConsecutiveForSubject', 'returned constraint of wrong kind'
        self.from_model_base(constraint=constraint)
        # load configuration as json string
        conf_data = json.loads(constraint.configuration)
        subject_id = conf_data['subject_id']
        consecutive_hours = conf_data['consecutive_hours']
        times = conf_data['times']
        self.configure(subject_id=subject_id, consecutive_hours=consecutive_hours, times=times)
