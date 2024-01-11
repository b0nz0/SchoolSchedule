from operator import itemgetter
import logging
import random
from typing import Tuple, Union, Any, List

from engine.struct import *
from engine.constraint import *


class SimpleEngineRand(Engine):
    MAX_REASSIGNMENTS = 2000

    def __init__(self) -> None:
        super().__init__()

    def load(self, school_year_id: int):
        rows = db.query.get_subjects_in_class_per_school_year(school_year_id=school_year_id)
        for row in rows:
            self.engine_support.load_assignment_from_subject_in_class(int(row))
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

        self.clear_assignments()

        # save remaining hours per assignment in class
        for assignment in self.engine_support.assignments.values():
            assignments_remaining[assignment] = assignment.data['hours_total']

        working = True
        # while we still have assignments with remaining hours
        while len([a for a in assignments_remaining.keys() if assignments_remaining[a] > 0]) > 0 and working:
            # pick randomly in assignments with remainig hours
            assignment = random.choice([a for a in assignments_remaining.keys() if assignments_remaining[a] > 0])
            persons_list = [x['person'] for x in assignment.data['persons']]
            persons_string = ",".join(persons_list)
            class_id = assignment.data['class_id']
            candidates = []
            subject = assignment.data['subject']
            logging.debug(f'cerco un candidato per la classe {class_id}-{subject}')
            for day in db.model.WeekDayEnum:
                for hour in range(1, 11):
                    if self.engine_support.get_assignment_in_calendar(class_id=class_id, day=day,
                                                               hour_ordinal=hour) == Calendar.AVAILABLE:
                        (score, constraint_scores) = self.evaluate_constraints(calendar_id=class_id,
                                                                               assignment=assignment, day=day,
                                                                               hour=hour)
                        logging.debug(f'update: score now = {score} (prof. {persons_string}, day {day.value}, \
                            hour {hour})')
                        if score >= 0:
                            logging.debug(f'candidato: score now = {score} (prof. {persons_string}, day {day.value}, \
                                hour {hour})')
                            if self._suggest_continuing and assignments_remaining[assignment] > 1:
                                candidates.append((score, constraint_scores, day, hour, True))
                            else:
                                candidates.append((score, constraint_scores, day, hour, False))
                    else:
                        pass
                    # logging.debug(f'skipping day {day.value}, hour {hour}')

            # get the highest score between possible candidates and assign it to the hour
            if len(candidates) == 0:
                if reassignments < SimpleEngineRand.MAX_REASSIGNMENTS:
                    (score, sugg_day, sugg_hour) = self._suggest_substitution(assignment)
                    if sugg_day != Calendar.UNAIVALABLE:
                        logging.debug(
                            f'impossibile trovare un candidato, provo una riassegnazione del {sugg_day} - ora {sugg_hour}')
                        candidate = self.engine_support.get_assignment_in_calendar(class_id=class_id, day=sugg_day,
                                                                            hour_ordinal=sugg_hour)
                        self.engine_support.deassign(class_id=class_id, day=sugg_day, hour_ordinal=sugg_hour)
                        assignments_remaining[candidate] = assignments_remaining[candidate] + 1
                        reassignments = reassignments + 1
                else:
                    subjects = ",".join([a.data['subject'] for a in assignments_remaining.keys()
                                         if assignments_remaining[a] > 0])
                    logging.error(f'impossibile trovare un candidato, già provate {reassignments} riassegnazioni. \
                        Rimangono fuori: {subjects}')
                    working = False
                    break
            else:
                (score, constraint_scores, day, hour, continuing) = sorted(candidates, key=itemgetter(0), reverse=True)[
                    0]
                logging.debug(f'best candidate: class={class_id}, score={score}, day={day.value}, hour={hour}')
                self.engine_support.assign(subject_in_class_id=assignment.subject_in_class_id,
                                    class_id=class_id, day=day, hour_ordinal=hour, score=score,
                                    constraint_scores=constraint_scores)
                assignments_remaining[assignment] = assignments_remaining[assignment] - 1
                # let's see if we can attach a hour after this one, as suggested
                if continuing:
                    if self.engine_support.get_assignment_in_calendar(class_id=class_id, day=day,
                                                               hour_ordinal=hour + 1) == Calendar.AVAILABLE:
                        (score, constraint_scores) = self.evaluate_constraints(calendar_id=class_id,
                                                                               assignment=assignment, day=day,
                                                                               hour=hour + 1)
                        if score >= 0:
                            logging.debug('can continue')
                            self.engine_support.assign(subject_in_class_id=assignment.subject_in_class_id,
                                                class_id=class_id, day=day, hour_ordinal=hour + 1, score=score,
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
            if c.has_trigger(trigger=assignment.data['subject_id'], trigger_type=Constraint.TRIGGER_SUBJECT):
                score = c.fire(self.engine_support, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
                constraint_scores.append((c, score))
                overall_score = overall_score + score
            for person in [x['person_id'] for x in assignment.data['persons']]:
                if c.has_trigger(trigger=person, trigger_type=Constraint.TRIGGER_PERSON):
                    score = c.fire(self.engine_support, calendar_id=calendar_id, assignment=assignment, day=day, hour=hour)
                    constraint_scores.append((c, score))
                    overall_score = overall_score + score
            suggest_continuing = suggest_continuing or c.suggest_continuing()
        self._suggest_continuing = suggest_continuing

        return (overall_score, constraint_scores)

    def _suggest_substitution(self, assignment):
        MAX = 1000000000
        lowest_score = (MAX, None, 0)
        class_id = assignment.data['class_id']
        for day in db.model.WeekDayEnum:
            for hour in range(1, 11):
                candidate = self.engine_support.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour)
                if candidate != Calendar.UNAIVALABLE and candidate != Calendar.AVAILABLE:
                    (score, constraint_scores) = self.engine_support.get_score(class_id=class_id, day=day, hour_ordinal=hour)
                    if score < lowest_score[0]:
                        lowest_score = (score, day, hour)
                    if score == lowest_score[0] and random.choice(
                            [True, False, False, False, False, False, False, False]):
                        lowest_score = (score, day, hour)
        if lowest_score[0] == MAX:
            return (MAX, Calendar.UNAIVALABLE, 0)
        else:
            return lowest_score

    def write_calendars_to_csv(self, filename):
        self.engine_support.write_calendars_to_csv(filename=filename)

    @property
    def closed(self):
        return self._closed
