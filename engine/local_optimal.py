from operator import itemgetter
import logging
import random
from engine.struct import *
from engine.constraint import *
from engine.simple_engine import SimpleEngine

class LocalOptimalEngine(Engine):

    MAX_REASSIGNMENTS = 2000

    def __init__(self) -> None:
        super().__init__()

    def load(self, school_year_id: int):
        rows = db.query.get_subjects_in_class_per_school_year(school_year_id=school_year_id)
        for row in rows:
            self._struct.load_assignment_from_subject_in_class(int(row))
        constraint = NonDuplicateConstraint()
        constraint.identifier = "non-duplicate"
        self._struct.constraints.add(constraint)
        constraint = NoComebacks()
        constraint.identifier = "no comebacks"        
        self._struct.constraints.add(constraint)

    def run(self):
        assignments_remaining = {}
        reassignments = 0

        # save remaining hours per assignment in class
        for assignment in self._struct.assignments.values():
            assignments_remaining[assignment] = assignment.data['hours_total']

        working = True
        # while we still have assignments with remaining hours
        while len([a for a in assignments_remaining.keys() if assignments_remaining[a] > 0]) > 0 and working:
            # cycle thru all free hours in each calendar to find a best score
            max_score = -1
            candidates = []
            for calendar_id in sorted(self._struct.get_calendar_ids(), reverse=random.choice([True, False])):
                for day in db.model.WeekDayEnum:
                    for hour in range(1, 11):  
                        if self._struct.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=hour) == Calendar.AVAILABLE:
                            for assignment in [a for a in assignments_remaining.keys() \
                                               if assignments_remaining[a] > 0]:
                                subject = assignment.data['subject']
                                persons_list = [x['person'] for x in assignment.data['persons']]
                                persons_string = ",".join(persons_list)
                                if reassignments > 80:
                                    pass
#                                    logging.debug('assignment class_id ' + str(assignment.data['class_id']) + ' subject ' + subject + \
#                                        '(' + persons_string + ') remaining ' + str(assignments_remaining[assignment]))
                                if assignment.data['class_id'] == calendar_id:
#                                    logging.debug(f'cerco classe {calendar_id}, giorno {day.value}, ora {hour}, materia {subject}')
                                    # find all non exhausted assignments for this class
                                    (score, constraint_scores) = self.evaluate_constraints(calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
                                    if score > max_score:
                                        max_score = score
                                        candidates = [(calendar_id, assignment, day, hour, constraint_scores)]
                                        logging.debug(f'candidato: score now = {score} (class {calendar_id}, prof. {persons_string}, day {day.value}, hour {hour})')
                                    elif score == max_score:
                                        candidates.append((calendar_id, assignment, day, hour, constraint_scores))
                                        logging.debug(f'candidato pari: score now = {score} (class {calendar_id}, prof. {persons_string}, day {day.value}, hour {hour})')                                        
                                    else:
                                        logging.debug(f'non candidato: score now = {score} < {max_score} (class {calendar_id}, prof. {persons_string}, day {day.value}, hour {hour})')

            # get the highest score between possible candidates and assign it to the hour
            if len(candidates) == 0:
                if reassignments < LocalOptimalEngine.MAX_REASSIGNMENTS:
                    for (score, class_id, sugg_day, sugg_hour) in self._suggest_substitution():
                        logging.debug(f'impossibile trovare un candidato, provo una riassegnazione della classe {class_id}@{sugg_day} - ora {sugg_hour}')
                        candidate = self._struct.get_assignment_in_calendar(class_id=class_id, day=sugg_day, hour_ordinal=sugg_hour)
                        self._struct.deassign(class_id=class_id, day=sugg_day, hour_ordinal=sugg_hour)
                        assignments_remaining[candidate] = assignments_remaining[candidate] + 1
                        reassignments = reassignments + 1
                else:
                    subjects = ",".join([a.data['subject'] for a in assignments_remaining.keys() if assignments_remaining[a] > 0])
                    logging.error(f'impossibile trovare un candidato, già provate {reassignments} riassegnazioni. Rimangono fuori: {subjects}')
                    working = False
                    break
            else:
                (calendar_id, assignment, day, hour, constraint_scores) = random.choice(candidates)
                logging.debug(f'assign best candidate: class={calendar_id}, score={max_score}, day={day.value}, hour={hour} out of {len(candidates)}')
                self._struct.assign(subject_in_class_id=assignment.subject_in_class_id,\
                                    class_id=calendar_id, day=day, hour_ordinal=hour, score=max_score, constraint_scores=constraint_scores)
                assignments_remaining[assignment] = assignments_remaining[assignment] - 1
                    # let's see if we can attach a hour after this one, as suggested
#                    if continuing:
#                        if self._struct.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour+1) == Calendar.AVAILABLE:
#                            score = self.evaluate_constraints(calendar_id=class_id, assignment=assignment, day=day, hour=hour+1)
#                            if score >= 0:
#                                logging.debug('can continue')
#                                self._struct.assign(subject_in_class_id=assignment.subject_in_class_id,\
#                                            class_id=class_id, day=day, hour_ordinal=hour+1, score=score)
#                                assignments_remaining[assignment] = assignments_remaining[assignment] - 1
        self._closed = working

    def evaluate_constraints(self, calendar_id, assignment, day, hour) -> int:
        overall_score = 0
        constraint_scores = []
        # if the constraint suggests to append a hour after the current one
        suggest_continuing = False
        for c in self._struct.constraints:
#            if c.has_trigger(None):
            score = c.fire(self._struct, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
            constraint_scores.append((c, score))
            overall_score = overall_score + score
#            if c.has_trigger(trigger=assignment.data['subject_id'], trigger_type=Constraint.TRIGGER_SUBJECT):
#                score = score + c.fire(self._struct, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
#            for person in [x['person_id'] for x in assignment.data['persons']]:                                        
#                if c.has_trigger(trigger=person, trigger_type=Constraint.TRIGGER_PERSON):
#                    score = score + c.fire(self._struct, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)                                        
#            suggest_continuing = suggest_continuing or c.suggest_continuing()                                      
#            self._suggest_continuing = suggest_continuing
        return (overall_score, constraint_scores)

    def _suggest_substitution(self):
        MAX = 1000000000
        lowest_score = MAX
        ret = []
        for class_id in self._struct.get_calendar_ids():
            for day in db.model.WeekDayEnum:
                for hour in range(1, 11):  
                    candidate = self._struct.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour)
                    if  candidate != Calendar.UNAIVALABLE and candidate != Calendar.AVAILABLE:
                        (score, constraint_scores) = self._struct.get_score(class_id=class_id, day=day, hour_ordinal=hour)
                        if score <= lowest_score:
                            ret.append((score, class_id, day, hour))
                            lowest_score = score
        return ret
    
    def write_calendars_to_csv(self, filename):
        self._struct.write_calendars_to_csv(filename=filename)
            
    @property
    def closed(self):
        return self._closed
    