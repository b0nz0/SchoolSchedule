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
        for i in range(1, 100):
            print(f'inizio 2nd round ({i})')
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
            if len(candidates) == 0:
                print('chiuso')
                break

            # candidates = sorted(candidates, key=itemgetter(3), reverse=True)
            candidates_free = [c for c in candidates if c[3] > 1]
            candidates_blocked = [c for c in candidates if c[3] <= 1]
            moved = False
            for assignment, day, hour, score in candidates_free:
                persons_str = ",".join([x['person'] for x in assignment.data['persons']])
                logging.debug(f'candidato per {persons_str} in classe ' +
                              self.class_support[assignment.data['class_id']]['identifier'] +
                              f': {day.value}  {hour} ora \t({score})')
                if score > 1:
                    logging.debug(f'provo ad assegnare per score {score}')
                    if self.manage_assignment(assignment, day=day, hour=hour):
                        moved = True
            random.shuffle(candidates_blocked)
            for assignment, day, hour, score in candidates_blocked:
                if score <= 1:
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
            print(f'remaining {new_remaining}')
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

            self.assignments_remaining[assignment] -= 1

            for pid in pids:
                self.person_support[pid]['busy'][day].append(hour)

            logging.debug('assegno classe ' + self.class_support[class_id]['identifier'] +
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

        # check #4: sum up all assignments for same subject in the day
        if assignment.data['max_hours_per_day'] is None:
            max_hours_per_day = 1
        else:
            max_hours_per_day = assignment.data['max_hours_per_day']
        count_hours = 0
        for xhour in range(1, 11):
            if self.engine_support.get_assignment_in_calendar(class_id=assignment.data['class_id'],
                                                                day=day, hour_ordinal=xhour) \
                                                                    == assignment:
                count_hours += 1
        if count_hours >= max_hours_per_day:
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

                assigned = False
                for assignment in assignments:
                    hour = 1
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
                                if other_hour - hour > 1 or hour - other_hour > 1:
                                    # no holes
                                    candidate = (False, 0)
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


    def write_calendars_to_csv(self, filename, filename_debug):
        self.engine_support.write_calendars_to_csv(filename=filename, filename_debug=filename_debug)

    @property
    def closed(self):
        return self._closed
