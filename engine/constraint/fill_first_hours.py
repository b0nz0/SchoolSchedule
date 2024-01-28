import db.model
from engine.struct import Constraint, Assignment, EngineSupport


class FillFirstHours(Constraint):
    """
    boost assigning to first hours
    """

    def __init__(self) -> None:
        super().__init__()
        self.score = 10
        self.weight = 20
        self.register_trigger(None)

    def fire(self, engine_support: EngineSupport, calendar_id: int = None, assignment: Assignment = None,
             day: db.model.WeekDayEnum = None, hour: int = None):
        assert assignment is not None, 'no assignment provided'
        assert hour is not None, 'no hour ordinal provided'

        return self.score - hour

    def to_model(self) -> db.model.Constraint:
        constraint = self.to_model_base()
        constraint.kind = 'FillFirstHours'
        return constraint

    def from_model(self, constraint: db.model.Constraint):
        assert constraint.kind == 'FillFirstHours', 'returned constraint of wrong kind'
        self.from_model_base(constraint=constraint)
