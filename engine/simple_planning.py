import copy
import logging
import random

import engine.constraint
from engine.constraint import *
from engine.struct import *


class SimplePlanningEngine(Engine):
    MAX_REASSIGNMENTS = 200

    def __init__(self) -> None:
        super().__init__()
        self.working = None
        self.engine_support_base = None
        self.person_support = None

    def load(self, school_year_id: int):
        rows = db.query.get_subjects_in_class_per_school_year(school_year_id=school_year_id)
        for row in rows:
            subject_in_class = db.query.get(db.model.SubjectInClass, int(row))
            self.engine_support.load_assignment_from_subject_in_class(subject_in_class)

        school_year = db.query.get(db.model.SchoolYear, school_year_id)
        subjects = db.query.get_subjects(school_id=school_year.school_id)
        for subject in subjects:
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
        logging.info('trying to plan a simple calendar')
        self.run_planner()
        if not self.closed:
            logging.error(f'Unable to plan a simple calendar')
            return

        logging.info('simple calendar planned')
        self.engine_support_base = self.engine_support
        self._struct = copy.copy(self.engine_support_base)

    def run_planner(self):
        assignments_remaining = {}
        reassignments = 0

        self.clear_assignments()

        all_days = set()
        for calendar in self.engine_support.calendars:
            for day in db.model.WeekDayEnum:
                if self.engine_support.get_assignment_in_calendar(
                        class_id=calendar, day=day, hour_ordinal=1) == Calendar.AVAILABLE:
                    all_days.add(day)

        self.person_support = dict()
        for pid in self.engine_support.persons.keys():
            self.person_support[pid] = dict()
            self.person_support[pid]['assignments'] = self.engine_support.persons[pid]
            self.person_support[pid]['days'] = list(all_days)
            self.person_support[pid]['busy'] = dict()

            for constraint in self.engine_support.constraints:
                if isinstance(constraint, engine.constraint.CalendarDays) and constraint.person_id == pid:
                    days = set()
                    for allowed_hour in constraint.allowed_hours_list:
                        days.add(allowed_hour[0])
                    self.person_support[pid]['days'] = list(days)

            for day in self.person_support[pid]['days']:
                self.person_support[pid]['busy'][day] = list()

        self.working = True
        for pid in self.person_support.keys():
            self.plan_person(pid=pid)

        self._closed = self.working

    def plan_person(self, pid):

        # save remaining hours per assignment in class
        assignments_remaining = dict()
        for assignment in self.person_support[pid]['assignments']:
            assignments_remaining[assignment] = assignment.data['hours_total']

        print(f'person {pid}')
        while True:
            assignments = [assignment for assignment in assignments_remaining.keys()
                           if assignments_remaining[assignment] > 0]
            if len(assignments) == 0:
                # no more assignments to do
                break
            for day in self.person_support[pid]['days']:
                hour = 1
                assigned = False
                for assignment in assignments:
                    # change day, assignment done
                    if assigned:
                        break
                    if assignments_remaining[assignment] == 0:
                        continue
                    class_id = assignment.data['class_id']
                    if assignment.data['max_hours_per_day']:
                        max_hours_per_day = assignment.data['max_hours_per_day']
                    else:
                        max_hours_per_day = 1
                    while hour < 11:
                        consecutive = 0
                        while consecutive < max_hours_per_day and assignments_remaining[assignment] > 0:
                            if self.engine_support.get_assignment_in_calendar(
                                    class_id=class_id, day=day, hour_ordinal=hour) == Calendar.AVAILABLE and \
                                    hour not in self.person_support[pid]['busy'][day]:
                                self.engine_support.assign(assignment.subject_in_class_id,
                                                           class_id=class_id,
                                                           day=day, hour_ordinal=hour, score=1,
                                                           constraint_scores=list((None, 0)))
                                assigned = True
                                self.person_support[pid]['busy'][day].append(hour)
                                print(f'assegno classe {class_id}, giorno: {day}, ora: {hour}')
                                assignments_remaining[assignment] -= 1
                            hour += 1
                            consecutive += 1
                        if consecutive == 0:
                            hour += 1

    def ___backup(self):

        # save remaining hours per assignment in class
        for assignment in self.engine_support.assignments.values():
            assignments_remaining[assignment] = assignment.data['hours_total']

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
                                # find all non-exhausted assignments for this class
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
                if reassignments < SimplePlanningEngine.MAX_REASSIGNMENTS:
                    (score, sugg_day, sugg_hour, sugg_class_id) = self._suggest_substitution()
                    if sugg_day != Calendar.UNAIVALABLE:
                        logging.debug(
                            f'impossibile trovare un candidato, provo una riassegnazione del {sugg_day} - ora {sugg_hour}')
                        candidate = self.engine_support.get_assignment_in_calendar(class_id=sugg_class_id, day=sugg_day,
                                                                                   hour_ordinal=sugg_hour)
                        self.engine_support.deassign(class_id=sugg_class_id, day=sugg_day, hour_ordinal=sugg_hour)
                        assignments_remaining[candidate] = assignments_remaining[candidate] + 1
                        reassignments = reassignments + 1
                else:
                    subjects = ",".join(
                        [a.data['subject'] + ' ' + str(a.data['year']) + ' ' + str(a.data['section']) +
                         ' (' + ",".join([x['person'] for x in a.data['persons']]) + ') '
                         for a in assignments_remaining.keys()
                         if assignments_remaining[a] > 0]
                    )
                    logging.error(
                        f'impossibile trovare un candidato, già provate {reassignments} riassegnazioni. \
                            Rimangono fuori: {subjects}')
                    working = False
                    break
            else:
                (calendar_id, assignment, day, hour, constraint_scores) = (
                    self.evaluate_candidates(candidates, assignments_remaining))
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
                if score != 0:
                    constraint_scores.append((c, score))
                overall_score = overall_score + score
                continue
            if c.has_trigger(trigger=assignment.data['subject_id'], trigger_type=Constraint.TRIGGER_SUBJECT):
                score = c.fire(self.engine_support, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
                if score != 0:
                    constraint_scores.append((c, score))
                overall_score = overall_score + score
                continue
            for person in [x['person_id'] for x in assignment.data['persons']]:
                if c.has_trigger(trigger=person, trigger_type=Constraint.TRIGGER_PERSON):
                    score = c.fire(self.engine_support, calendar_id=calendar_id, assignment=assignment, day=day,
                                   hour=hour)
                    if score != 0:
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

    def _suggest_substitution(self):
        MAX = 1000000000
        lowest_score = (MAX, None, 0, 0)
        for class_id in self.engine_support.get_calendar_ids():
            for day in db.model.WeekDayEnum:
                for hour in range(1, 11):
                    candidate = self.engine_support.get_assignment_in_calendar(class_id=class_id, day=day,
                                                                               hour_ordinal=hour)
                    if candidate != Calendar.UNAIVALABLE and candidate != Calendar.AVAILABLE:
                        (score, constraint_scores) = self.engine_support.get_score(class_id=class_id, day=day,
                                                                                   hour_ordinal=hour)
                        # if score < lowest_score[0]:
                        #     lowest_score = (score, day, hour)
                        # if score == lowest_score[0] and random.choice(
                        #         [True, False, False, False, False, False, False, False]):
                        #     lowest_score = (score, day, hour)
                        if score < 11:
                            if lowest_score[1] is None:
                                lowest_score = (score, day, hour, class_id)
                            else:
                                if random.choice(
                                        [True, False, False, False, False, False, False, False]):
                                    lowest_score = (score, day, hour, class_id)
        if lowest_score[0] == MAX:
            return (MAX, Calendar.UNAIVALABLE, 0, 0)
        else:
            return lowest_score

    def write_calendars_to_csv(self, filename, filename_debug):
        self.engine_support.write_calendars_to_csv(filename=filename, filename_debug=filename_debug)

    @property
    def closed(self):
        return self._closed
