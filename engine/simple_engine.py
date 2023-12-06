from operator import itemgetter
from engine.struct import *
from engine.constraint import *

class SimpleEngine():

    def __init__(self) -> None:
        self._struct = EngineSupport()

    def load(self, school_year_id: int):
        rows = db.query.get_subjects_in_class_per_school_year(school_year_id=school_year_id)
        for row in rows:
            self._struct.load_assignment_from_subject_in_class(int(row))
        constraint = NonDuplicateConstraint()
        self._struct.constraints.add(constraint)

    def run(self):
        assignments_remaining = {}

        # save remaining hours per assignment in class
        for assignment in self._struct.assignments.values():
            assignments_remaining[assignment] = assignment.data['hours_total']

        # while we still have assignments with remaining hours
        while len([a for a in assignments_remaining.keys() if assignments_remaining[a] > 0]) > 0:
            # cycle thru all assignments with remainig hours
            for assignment in [a for a in assignments_remaining.keys() if assignments_remaining[a] > 0]:
                persons_list = [x['person'] for x in assignment.data['persons']]
                persons_string = ",".join(persons_list)
                class_id = assignment.data['class_id']
                calendar = self._struct.get_calendar(class_id=class_id)
                candidates = []
                for day in db.model.WeekDayEnum:
                    for hour in range(1, 11):  
                        if self._struct.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour) == Calendar.AVAILABLE:
                            score = 0
                            for c in self._struct.constraints:
                                if c.has_trigger(None):
                                    score = score + c.fire(self._struct, assignment=assignment, day=day, hour=hour)
                                    print(f'score now = {score} (prof. {persons_string})')
                            if score >= 0:
                                candidates.append((score, day, hour))
                (score, day, hour) = sorted(candidates, key=itemgetter(0), reverse=True)[0]
                print(f'best candidate: class={class_id}, score={score}, day={day.value}, hour={hour}')
                self._struct.assign(subject_in_class_id=assignment.subject_in_class_id,\
                                    class_id=assignment.data['class_id'], \
                                    day=day, hour_ordinal=hour)
                assignments_remaining[assignment] = assignments_remaining[assignment] - 1