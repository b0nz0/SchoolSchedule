import logging
import random

from engine.constraint import *
from engine.struct import *


class LocalOptimalEngine(Engine):
    MAX_REASSIGNMENTS = 200

    def __init__(self) -> None:
        super().__init__()
        self.last_assignments = None

    def load(self, school_year_id: int):
        rows = db.query.get_subjects_in_class_per_school_year(school_year_id=school_year_id)
        for row in rows:
            subject_in_class = db.query.get(db.model.SubjectInClass, int(row))
            self.engine_support.load_assignment_from_subject_in_class(subject_in_class)
            subject = db.query.get(db.model.Subject, subject_in_class.subject_id)
            if subject.preferred_consecutive_hours is not None:
                constraint = MaximumConsecutiveForSubject()
                constraint.identifier = 'max consecutive ' + subject.identifier
                constraint.configure(subject_id=subject.id, consecutive_hours=subject.preferred_consecutive_hours)
                self.engine_support.constraints.add(constraint)
        constraint = NonDuplicateConstraint()
        constraint.identifier = "non-duplicate"
        self.engine_support.constraints.add(constraint)
        constraint = NoComebacks()
        constraint.identifier = "no comebacks"
        self.engine_support.constraints.add(constraint)
        constraint = FillFirstHours()
        constraint.identifier = "riempi prime ore"
        self.engine_support.constraints.add(constraint)

    def run(self):
        assignments_remaining = {}
        reassignments = 0
        self.last_assignments = {}

        self.clear_assignments()

        for calendar_id in self.engine_support.get_calendar_ids():
            self.last_assignments[calendar_id] = []

        # save remaining hours per assignment in class
        for assignment in self.engine_support.assignments.values():
            assignments_remaining[assignment] = assignment.data['hours_total']

        working = True
        odd = True
        # while we still have assignments with remaining hours
        while len([a for a in assignments_remaining.keys() if assignments_remaining[a] > 0]) > 0 and working:
            # cycle thru all free hours in each calendar to find a best score
            max_score = -1
            candidates = []
            odd = not odd
            for calendar_id in sorted(self.engine_support.get_calendar_ids(), reverse=odd):
                for day in db.model.WeekDayEnum:
                    for hour in range(1, 11):
                        if self.engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day,
                                                                   hour_ordinal=hour) == Calendar.AVAILABLE:
                            for assignment in [a for a in assignments_remaining.keys() \
                                               if assignments_remaining[a] > 0 and a.data['class_id'] == calendar_id]:
                                subject = assignment.data['subject']
                                persons_list = [x['person'] for x in assignment.data['persons']]
                                persons_string = ",".join(persons_list)
                                if reassignments > 80:
                                    pass
                                #                                    logging.debug('assignment class_id ' + str(assignment.data['class_id']) + ' subject ' + subject + \
                                #                                        '(' + persons_string + ') remaining ' + str(assignments_remaining[assignment]))
                                #                                    logging.debug(f'cerco classe {calendar_id}, giorno {day.value}, ora {hour}, materia {subject}')
                                # find all non exhausted assignments for this class
                                (score, constraint_scores) = self.evaluate_constraints(calendar_id=calendar_id,
                                                                                       assignment=assignment, day=day,
                                                                                       hour=hour)
                                if score > max_score:
                                    max_score = score
                                    candidates = [(calendar_id, assignment, day, hour, constraint_scores)]
                                    logging.debug(
                                        f'candidato: score now = {score} (class {calendar_id}, prof. {persons_string}, day {day.value}, hour {hour})')
                                elif score == max_score:
                                    candidates.append((calendar_id, assignment, day, hour, constraint_scores))
                                    logging.debug(
                                        f'candidato pari: score now = {score} (class {calendar_id}, prof. {persons_string}, day {day.value}, hour {hour})')
                                else:
                                    logging.debug(
                                        f'non candidato: score now = {score} < {max_score} (class {calendar_id}, prof. {persons_string}, day {day.value}, hour {hour})')

            # get the highest score between possible candidates and assign it to the hour
            if len(candidates) == 0:
                if reassignments < LocalOptimalEngine.MAX_REASSIGNMENTS:
                    for (score, class_id, sugg_day, sugg_hour) in self.suggest_substitution():
                        logging.debug(
                            f'impossibile trovare un candidato, provo una riassegnazione della classe {class_id}@{sugg_day} - ora {sugg_hour}')
                        candidate = self.engine_support.get_assignment_in_calendar(class_id=class_id, day=sugg_day,
                                                                            hour_ordinal=sugg_hour)
                        if type(candidate) == Assignment:
                            self.engine_support.deassign(class_id=class_id, day=sugg_day, hour_ordinal=sugg_hour)
                            assignments_remaining[candidate] = assignments_remaining[candidate] + 1
                            reassignments = reassignments + 1
                else:
                    subjects = ",".join(
                        [a.data['subject'] for a in assignments_remaining.keys() if assignments_remaining[a] > 0])
                    logging.error(
                        f'impossibile trovare un candidato, già provate {reassignments} riassegnazioni. \
                            Rimangono fuori: {subjects}')
                    working = False
                    break
            else:
                (calendar_id, assignment, day, hour, constraint_scores) = self.evaluate_candidates(candidates,
                                                                                                   assignments_remaining)
                self.last_assignments[calendar_id].append((calendar_id, assignment, day, hour, constraint_scores))
                logging.debug(
                    f'assign best candidate: class={calendar_id}, score={max_score}, day={day.value}, \
                        hour={hour} out of {len(candidates)}')
                self.engine_support.assign(subject_in_class_id=assignment.subject_in_class_id,
                                    class_id=calendar_id, day=day, hour_ordinal=hour, score=max_score,
                                    constraint_scores=constraint_scores)
                assignments_remaining[assignment] = assignments_remaining[assignment] - 1

        self._closed = working

    def evaluate_constraints(self, calendar_id, assignment, day, hour):
        overall_score = 0
        constraint_scores = []
        # if the constraint suggests to append a hour after the current one
        suggest_continuing = False
        for c in self.engine_support.constraints:
            if c.has_trigger(None):
                score = c.fire(self.engine_support, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
                constraint_scores.append((c, score))
                overall_score = overall_score + score
                continue
            if c.has_trigger(trigger=assignment.data['subject_id'], trigger_type=Constraint.TRIGGER_SUBJECT):
                score = c.fire(self.engine_support, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
                constraint_scores.append((c, score))
                overall_score = overall_score + score
                continue
            for person in [x['person_id'] for x in assignment.data['persons']]:
                if c.has_trigger(trigger=person, trigger_type=Constraint.TRIGGER_PERSON):
                    score = c.fire(self.engine_support, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
                    constraint_scores.append((c, score))
                    overall_score = overall_score + score
                    continue
        return (overall_score, constraint_scores)

    def evaluate_candidates(self, candidates, assignments_remaining):
        assert len(candidates) > 0, 'no candidates left'
        return random.choice(candidates)

    '''        for prop in candidates:
            # enough assignments to backtrack?
            if len(self.last_assignments[prop[0]]) < 5: return prop
            if prop[1] not in [x[1] for x in self.last_assignments[prop[0]][-5:]]:
                return prop
        logging.info('cycling thru backtracking')
        return candidates[0]

        for (class_id_cand, assignment, day_cand, hour_cand, constraint_scores_cand) in candidates:
            # evaluate only assignments with remaining hours
            if assignments_remaining[assignment] == 1:
                return (class_id_cand, assignment, day_cand, hour_cand, constraint_scores_cand)
            # try assigning and let's see what happens to further assignments
            self.engine_support.assign(subject_in_class_id=assignment.subject_in_class_id,\
                                    class_id=class_id_cand, day=day_cand, hour_ordinal=hour_cand, score=1, constraint_scores=constraint_scores_cand)
            positives = 0
            for calendar_id in self.engine_support.get_calendar_ids():
                for day in db.model.WeekDayEnum:
                    for hour in range(1, 11):  
                        if self.engine_support.get_assignment_in_calendar(class_id=calendar_id, day=day, hour_ordinal=hour) == Calendar.AVAILABLE:
                            (score, constraint_scores) = self.evaluate_constraints(calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
                            if score > 0: positives = positives + 1
            self.engine_support.deassign(class_id=class_id_cand, day=day_cand, hour_ordinal=hour_cand)
            # at least another assignment is possible
            if positives > 0: 
                return (class_id_cand, assignment, day_cand, hour_cand, constraint_scores_cand)
        
        logging.info('no candidates with score < 0')
        return candidates[0]
    '''

    def suggest_substitution(self):
        ret = []
        for calendar_id in self.engine_support.get_calendar_ids():
            for (class_id, assignment, day, hour, constraint_scores) in self.last_assignments[calendar_id][-5:]:
                ret.append((0, class_id, day, hour))
        return ret
        '''# a simple backtracking
        (calendar_id, assignment, day, hour, constraint_scores) = self.last_assignments[-1]
        return [(0, calendar_id, day, hour)]
        MAX = 1000000000
        lowest_score = MAX
        ret = []
        for class_id in self.engine_support.get_calendar_ids():
            for day in db.model.WeekDayEnum:
                for hour in range(1, 11):  
                    candidate = self.engine_support.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour)
                    if  candidate != Calendar.UNAIVALABLE and candidate != Calendar.AVAILABLE:
                        (score, constraint_scores) = self.engine_support.get_score(class_id=class_id, day=day, hour_ordinal=hour)
                        if score <= lowest_score:
                            ret.append((score, class_id, day, hour))
                            lowest_score = score
        return ret
        '''

    def write_calendars_to_csv(self, filename):
        self.engine_support.write_calendars_to_csv(filename=filename)

    @property
    def closed(self):
        return self._closed
