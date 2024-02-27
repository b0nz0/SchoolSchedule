import copy
import logging
import random
from operator import itemgetter

import engine.constraint
from engine.constraint import *
from engine.struct import *


class SimplePlanningEngine(Engine):
    MAX_REASSIGNMENTS = 200

    def __init__(self) -> None:
        super().__init__()
        self.assignments_remaining = None
        self.assignments_remaining = None
        self.all_days = None
        self.working = None
        self.engine_support_base = None
        self.person_support = None
        self.class_support = None
        self.subject_support = None

    def load(self, school_year_id: int):
        rows = db.query.get_subjects_in_class_per_school_year(school_year_id=school_year_id)
        for row in rows:
            subject_in_class = db.query.get(db.model.SubjectInClass, int(row))
            self.engine_support.load_assignment_from_subject_in_class(subject_in_class)

        # fill in a support structure for subjects and create specific constraints for preferred consecutive hours
        self.subject_support = dict()
        school_year = db.query.get(db.model.SchoolYear, school_year_id)
        subjects = db.query.get_subjects(school_id=school_year.school_id)
        for subject in subjects:
            self.subject_support[subject.id] = dict()
            self.subject_support[subject.id]['identifier'] = subject.identifier
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

        # all available days in assignments
        self.all_days = set()
        for calendar in self.engine_support.calendars:
            for day in db.model.WeekDayEnum:
                if self.engine_support.get_assignment_in_calendar(
                        class_id=calendar, day=day, hour_ordinal=1) == Calendar.AVAILABLE:
                    self.all_days.add(day)

        # fill in a support structure for persons
        self.person_support = dict()
        for pid in self.engine_support.persons.keys():
            self.person_support[pid] = dict()
            person = db.query.get(db.model.Person, id=pid)
            self.person_support[pid]['fullname'] = person.fullname
            self.person_support[pid]['days'] = list(self.all_days)
            self.person_support[pid]['assignments'] = self.engine_support.persons[pid]

            # in case not all days are available
            for constraint in self.engine_support.constraints:
                if isinstance(constraint, engine.constraint.CalendarDays) and constraint.person_id == pid:
                    days = set()
                    for allowed_hour in constraint.allowed_hours_list:
                        days.add(allowed_hour[0])
                    self.person_support[pid]['days'] = list(days)

        self.class_support = dict()
        classes = db.query.get_classes(schoolyear_id=school_year_id)
        for class_ in classes:
            self.class_support[class_.id] = dict()
            self.class_support[class_.id]['identifier'] = str(class_)

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
        reassignments = 0

        self.clear_assignments()

        for pid in self.person_support.keys():
            self.person_support[pid]['busy'] = dict()
            for day in self.person_support[pid]['days']:
                self.person_support[pid]['busy'][day] = list()

        # save remaining hours per assignment in class
        self.assignments_remaining = dict()
        for assignment in self.engine_support.assignments.values():
            self.assignments_remaining[assignment] = assignment.data['hours_total']

        # 1st round
        self.working = True
        for pid in self.person_support.keys():
            self.plan_person(pid=pid)
        print('fine 1 round')
        # let's try who has days constraints before others
        # for pid in [k for k in self.person_support.keys() if len(self.person_support[k]['days']) < len(self.all_days)]:
        #     self.plan_person(pid=pid)
        # for pid in [k for k in self.person_support.keys() if len(self.person_support[k]['days']) == len(self.all_days)]:
        #     self.plan_person(pid=pid)

        # 2nd round:
        tot_remaining = sum(self.assignments_remaining.values())
        for i in range(1, 500):
            print('inizio 2nd round')
            for (assignment, remaining) in copy.copy(self.assignments_remaining).items():
                if remaining == 0:
                    self.assignments_remaining.pop(assignment)
                    continue
                persons = ",".join([x['person'] for x in assignment.data['persons']])
                print('per ' + persons + ' rimangono ' + str(self.assignments_remaining[assignment]) + ' ore in ' +
                      self.class_support[assignment.data['class_id']]['identifier'])

            candidates = list()
            for assignment in [x for (x, r) in self.assignments_remaining.items() if r > 0]:
                candidates.extend(self.find_candidate(assignment))

            candidates = sorted(candidates, key=itemgetter(3), reverse=True)
            moved = False
            for assignment, day, hour, score in candidates:
                persons_str = ",".join([x['person'] for x in assignment.data['persons']])
                logging.debug(f'candidato per {persons_str} in classe ' +
                              self.class_support[assignment.data['class_id']]['identifier'] +
                              f': {day.value}  {hour} ora \t({score})')
                if score > 1:
                    if self.manage_assignment(assignment, day=day, hour=hour):
                        moved = True
                else:
                    to_swap_assignment = self.engine_support.get_assignment_in_calendar(
                        class_id=assignment.data['class_id'], day=day, hour_ordinal=hour)
                    self.remove_assignment(assignment=to_swap_assignment, day=day, hour=hour)
                    # to_swap_day, to_swap_hour = self.get_all_slots_for_assignment(assignment)[0]
                    if self.manage_assignment(assignment, day=day, hour=hour):
                        moved = True
                        break
                    else:
                        assert self.manage_assignment(to_swap_assignment, day=day, hour=hour) is True, \
                            'unhandled problem in restoring assignment'

            # let's see if we moved on
            new_remaining = sum(self.assignments_remaining.values())
            # if not moved:
            #     print(f'impossibile procedere, rimangono {tot_remaining} assegnazioni fuori')
            #     break
            # else:
            #     tot_remaining = new_remaining

        self._closed = self.working

    def manage_assignment(self, assignment, day, hour) -> bool:
        class_id = assignment.data['class_id']
        pids = [x['person_id'] for x in assignment.data['persons']]

        if self.can_assign(assignment, day, hour):
            self.engine_support.assign(assignment.subject_in_class_id,
                                       class_id=class_id,
                                       day=day, hour_ordinal=hour, score=1,
                                       constraint_scores=list((None, 0)))

            if assignment in self.assignments_remaining.keys():
                self.assignments_remaining[assignment] -= 1

            for pid in pids:
                self.person_support[pid]['busy'][day].append(hour)

            print('assegno classe ' + self.class_support[class_id]['identifier'] +
                  f', giorno: {day.value}, ora: {hour}')
            return True
        else:
            return False

    def remove_assignment(self, assignment, day, hour):
        class_id = assignment.data['class_id']
        pids = [x['person_id'] for x in assignment.data['persons']]

        self.engine_support.deassign(class_id=class_id,
                                     day=day, hour_ordinal=hour)
        if assignment in self.assignments_remaining.keys():
            self.assignments_remaining[assignment] += 1
        else:
            self.assignments_remaining[assignment] = 1

        for pid in pids:
            self.person_support[pid]['busy'][day].remove(hour)

        logging.debug('rimossa assegnazione classe ' + self.class_support[class_id]['identifier'] +
                      f', giorno: {day}, ora: {hour}')

    def can_assign(self, assignment, day, hour, check_availability=True) -> bool:
        class_id = assignment.data['class_id']
        pids = [x['person_id'] for x in assignment.data['persons']]

        # can assign?

        # check #1: no other assignments for persons
        for pid in pids:
            if hour in self.person_support[pid]['busy'][day]:
                return False

        # check #2: slot is free. Check only if parameter is True
        if check_availability and self.engine_support.get_assignment_in_calendar(
                class_id=class_id, day=day, hour_ordinal=hour) != Calendar.AVAILABLE:
            return False

        # check #3: still have hours to assign
        if check_availability and self.assignments_remaining[assignment] < 1:
            return False

        # checks over, we can assign!
        return True

    def swap_assign(self, assignment_from, day_from, hour_from, assignment_to, day_to, hour_to) -> bool:
        if self.can_assign(assignment_from, day_to, hour_to, check_availability=False) and \
                self.can_assign(assignment_to, day_from, hour_from, check_availability=False):
            self.remove_assignment(assignment_from, day_from, hour_from)
            self.remove_assignment(assignment_to, day_to, hour_to)
            assert self.manage_assignment(assignment_from, day_to, hour_to) is True, 'unhandled problem in assignment'
            assert self.manage_assignment(assignment_to, day_from, hour_from) is True, 'unhandled problem in assignment'
            return True
        else:
            return False

    def get_all_slots_for_assignment(self, assignment, perform_random=False):
        class_id = assignment.data['class_id']
        slots = list()
        for day in db.model.WeekDayEnum:
            for hour in range(1, 11):
                if self.engine_support.get_assignment_in_calendar(class_id=class_id,
                                                                  day=day, hour_ordinal=hour) == assignment:
                    slots.append((day, hour))
        if perform_random:
            random.shuffle(slots)
        return slots

    def plan_person(self, pid):

        print('person ' + self.person_support[pid]['fullname'])

        while True:
            # let's see if we have still room for any assignment
            available = False

            assignments = [assignment for (assignment, remaining) in self.assignments_remaining.items()
                           if remaining > 0 and pid in [x['person_id'] for x in assignment.data['persons']]]
            if len(assignments) == 0:
                # no more assignments to do
                available = True
                logging.debug('done')
                break

            for day in self.person_support[pid]['days']:

                logging.debug(f'in {day} evaluating {len(assignments)} assignments')

                hour = 1
                assigned = False
                for assignment in assignments:
                    # change day, assignment done
                    if assigned:
                        break
                    if self.assignments_remaining[assignment] == 0:
                        continue
                    class_id = assignment.data['class_id']
                    if assignment.data['max_hours_per_day']:
                        max_hours_per_day = assignment.data['max_hours_per_day']
                    else:
                        max_hours_per_day = 1
                    while hour < 11:
                        consecutive = 0
                        while consecutive < max_hours_per_day and self.assignments_remaining[
                            assignment] > 0 and hour < 11:
                            if self.manage_assignment(assignment, day=day, hour=hour):
                                assigned = True
                                available = True
                                consecutive += 1
                            hour += 1
                        if assigned:
                            break

            # no hour available on candidate days, the calendar does not close
            if not available:
                self.working = False
                logging.info('unable to find availability for person ' + self.person_support[pid]['fullname'])
                # for assignment in assignments:
                #    self.assignments_out[assignment] = assignments_remaining[assignment]
                return
            else:
                logging.debug('continuing')

    def find_candidate(self, assignment):
        pids = [x['person_id'] for x in assignment.data['persons']]
        candidates = list()

        for day in self.all_days:
            for hour in range(1, 11):
                candidate = (False, 0)
                for pid in pids:
                    if day not in self.person_support[pid]['days']:
                        candidate = (False, 0)
                        continue
                    if hour in self.person_support[pid]['busy'][day]:
                        candidate = (False, 0)
                        continue
                    if self.engine_support.get_assignment_in_calendar(assignment.data['class_id'],
                                                                      day=day,
                                                                      hour_ordinal=hour) == Calendar.UNAIVALABLE:
                        candidate = (False, 0)
                        continue

                    # let's see if he/she is present in the class the same day
                    in_class = 0
                    for other_hour in range(1, 11):
                        if other_hour == hour:
                            continue
                        alt_assignment = self.engine_support.get_assignment_in_calendar(assignment.data['class_id'],
                                                                                        day=day,
                                                                                        hour_ordinal=other_hour)
                        if alt_assignment != Calendar.AVAILABLE and alt_assignment != Calendar.UNAIVALABLE:
                            if pid in [x['person_id'] for x in alt_assignment.data['persons']]:
                                if other_hour - hour > 1 or hour - other_hour < 1:
                                    # no holes
                                    break
                                else:
                                    in_class += 1

                    if assignment.data['max_hours_per_day'] is None:
                        max_hours_per_day = 1
                    else:
                        max_hours_per_day = assignment.data['max_hours_per_day']
                    if in_class < max_hours_per_day:
                        # still room to assign this day in this class
                        if self.engine_support.get_assignment_in_calendar(assignment.data['class_id'],
                                                                          day=day,
                                                                          hour_ordinal=hour) == Calendar.AVAILABLE:
                            candidate = (True, 10)
                        else:
                            candidate = (True, candidate[1] + 1)
                    else:
                        candidate = (False, 0)

                if candidate[0]:
                    candidates.append((assignment, day, hour, candidate[1]))

        return candidates

    def __plan_person(self, pid):

        # save remaining hours per assignment in class
        assignments_remaining = dict()
        for assignment in self.person_support[pid]['assignments']:
            assignments_remaining[assignment] = assignment.data['hours_total']

        print(f'person {pid}')
        while True:
            assignments = [assignment for assignment in assignments_remaining.keys()
                           if assignments_remaining[assignment] > 0]

            # let's see if we have still room for any assignment
            available = False
            for assignment in assignments:
                for day in self.person_support[pid]['days']:
                    for hour in range(1, 11):
                        if self.engine_support.get_assignment_in_calendar(
                                class_id=assignment.data['class_id'], day=day, hour_ordinal=hour) == Calendar.AVAILABLE:
                            print('found availability')
                            available = True
                            break
                    if available:
                        break
                if available:
                    break

            # no hour available on candidate days, the calendar does not close
            if not available:
                self.working = False
                print(f'unable to find availability for person {pid}')
                return

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
