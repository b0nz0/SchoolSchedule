from engine.struct import *
from db.model import DailyHour, WeekDayEnum

class NoComebacks(Constraint):
    
    def __init__(self) -> None:
        super().__init__()
        self.score = -20
        self.weight = 20
        self.register_trigger(None)

    def fire(self, engine_support: EngineSupport, calendar_id:int=None, assignment:Assignment=None, day:WeekDayEnum=None, hour:int=None):
        assert calendar_id != None, 'no calendar provided'
        assert assignment != None, 'no assignment provided'
        assert day != None, 'no weekday provided'
        assert hour != None, 'no hour ordinal provided'

        # get all the persons in this assignment
        persons = [x['person_id'] for x in assignment.data['persons']]
        
        # cycle thru the hours before this one in the same day
        for hour in range(1, hour-1):  
            ass_in_calendar = engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=hour)
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

