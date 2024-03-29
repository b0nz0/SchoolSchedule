import db.query
import db.model


class Assignment:

    def __init__(self, id) -> None:
        self._id = id
        self._subject_in_class_id = 0
        self._data = dict()
        self._score = 0

    def __repr__(self):
        ret = str()
        ret = ret + self._data['subject'] + ' in '
        ret = ret + self._data['year'] + ' '
        ret = ret + self._data['section'] + ' '
        ret = ret + '(' + self.persons + ')'
        return ret

    @property
    def id(self):
        return self._id

    @property
    def subject_in_class_id(self):
        return self._subject_in_class_id

    @subject_in_class_id.setter
    def subject_in_class_id(self, subject_in_class_id):
        self._subject_in_class_id = subject_in_class_id

    @property
    def data(self):
        return self._data

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def persons(self) -> str:
        return ",".join([x['person'] for x in self._data['persons']])

    @property
    def person_ids(self):
        return [x['person_id'] for x in self._data['persons']]

    @property
    def class_id(self) -> int:
        return self._data['class_id']


class Calendar:
    UNAIVALABLE = -100
    AVAILABLE = -1

    def __init__(self, class_id) -> None:
        self._class_id = class_id
        self._days = {}

    def load(self, plan_id: int):
        if len(self._days.keys()) > 0:
            print(f'Calendario {self.class_id} già caricato. Sovrascrivo\n')
        for day in db.model.WeekDayEnum:
            self._days[day] = {}
            for hour in range(1, 11):
                self._days[day][hour] = Calendar.UNAIVALABLE

        plan = db.query.get_plan(plan_id)
        if plan:
            for day in plan.keys():
                for daily_hour in plan[day]:
                    self._days[day][daily_hour.ordinal] = Calendar.AVAILABLE
        else:
            print(f'Plan ID {plan_id} non trovato\n')

    def day(self, day_id):
        if day_id in self._days.keys():
            return self._days[day_id]
        else:
            return None

    @property
    def class_id(self):
        return self._class_id


class Constraint:
    TRIGGER_ALWAYS = 0
    TRIGGER_PERSON = 1
    TRIGGER_CLASS = 2
    TRIGGER_ROOM = 3
    TRIGGER_SUBJECT = 4

    TRIGGER_TYPES = (
        TRIGGER_ALWAYS,
        TRIGGER_PERSON,
        TRIGGER_CLASS,
        TRIGGER_ROOM,
        TRIGGER_SUBJECT
    )

    REGISTERED_CONSTRAINTS = []

    def __init__(self) -> None:
        self._id = None
        self._triggers = {}
        for ctype in Constraint.TRIGGER_TYPES:
            self._triggers[ctype] = set()
        self._weight = 0
        self._school_year = None
        self._score = 0
        self._identifier = ''

    def get_triggers(self, trigger_type=None):
        if trigger_type in Constraint.TRIGGER_TYPES:
            return self._triggers[trigger_type]
        else:
            return self._triggers

    def register_trigger(self, trigger, trigger_type=TRIGGER_ALWAYS):
        assert trigger_type in Constraint.TRIGGER_TYPES, f'Attempt to add trigger <{trigger}> to non-existent type {trigger_type}'
        self._triggers[trigger_type].add(trigger)

    def delete_trigger(self, trigger, trigger_type=TRIGGER_ALWAYS):
        assert trigger_type in Constraint.TRIGGER_TYPES, f'Attempt to remove trigger <{trigger}> to non-existent type {trigger_type}'
        self._triggers[trigger_type].discard(trigger)

    def has_trigger(self, trigger, trigger_type=TRIGGER_ALWAYS):
        assert trigger_type in Constraint.TRIGGER_TYPES, f'Attempt to check trigger <{trigger}> to non-existent type {trigger_type}'
        if trigger_type == Constraint.TRIGGER_ALWAYS and len(self._triggers[Constraint.TRIGGER_ALWAYS]) > 0:
            return True
        return trigger in self._triggers[trigger_type]

    def fire(self, engine_support, calendar_id=None, assignment_id=None, day=None, hour=None):
        print('WARNING: fired superclass constraint')

    def suggest_continuing(self):
        return False

    def to_model(self) -> db.model.Constraint:
        pass

    def from_model(self, constraint: db.model.Constraint):
        pass

    def to_model_base(self) -> db.model.Constraint:
        if self.id is not None:
            constraint = db.query.get(db.model.Constraint, int(self.id))
        else:
            constraint = db.model.Constraint()
        constraint.identifier = self.identifier
        constraint.kind = 'Base'
        constraint.school_year_id = self.school_year.id
        constraint.score = self.score
        constraint.configuration = ''
        return constraint

    def from_model_base(self, constraint: db.model.Constraint):
        self.id = constraint.id
        self.identifier = constraint.identifier
        self.score = constraint.score
        self.school_year = db.query.get(db.model.SchoolYear, constraint.school_year_id)

    @classmethod
    def load_registered_constraints(cls):
        cls.REGISTERED_CONSTRAINTS = []
        cls.REGISTERED_CONSTRAINTS.append({'classname': 'NoComebacks', 'shortname': 'NoComebacks',
                                           'longname': 'No rientri'})
        cls.REGISTERED_CONSTRAINTS.append({'classname': 'NonDuplicateConstraint', 'shortname': 'NonDuplicateConstraint',
                                           'longname': 'No sovrapposizioni'})
        cls.REGISTERED_CONSTRAINTS.append({'classname': 'FillFirstHours', 'shortname': 'FillFirstHours',
                                           'longname': 'Riempire le prime ore'})
        cls.REGISTERED_CONSTRAINTS.append({'classname': 'MultipleConsecutiveForSubject',
                                           'shortname': 'MultipleConsecutiveForSubject',
                                           'longname': 'Coppia compito'})
        cls.REGISTERED_CONSTRAINTS.append({'classname': 'Boost', 'shortname': 'Boost',
                                           'longname': 'Aumenta probabilità'})
        cls.REGISTERED_CONSTRAINTS.append({'classname': 'CalendarDays', 'shortname': 'CalendarDays',
                                           'longname': 'Giorni disponibili'})
        cls.REGISTERED_CONSTRAINTS.append({'classname': 'MaximumConsecutiveForSubject',
                                           'shortname': 'MaximumConsecutiveForSubject',
                                           'longname': 'Limita ore consecutive'})
        cls.REGISTERED_CONSTRAINTS.append({'classname': 'MaximumDaysForPerson', 'shortname': 'MaximumDaysForPerson',
                                           'longname': 'Giorni massimi a settimana'})

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def school_year(self):
        return self._school_year

    @school_year.setter
    def school_year(self, school_year):
        self._school_year = school_year

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    def __repr__(self) -> str:
        return f'{self.identifier}'


class EngineSupport:

    def __init__(self) -> None:
        self._calendars = {}
        self._assignments = {}
        self._constraints = set()
        self._persons = {}
        self._scores = {}

    def get_assignment(self, subject_in_class_id: int):
        if subject_in_class_id in self._assignments.keys():
            return self._assignments[subject_in_class_id]
        else:
            self._assignments[subject_in_class_id] = Assignment(id=subject_in_class_id)
            return self._assignments[subject_in_class_id]

    def load_assignment_from_subject_in_class(self, subject_in_class: db.model.SubjectInClass):
        assignment = self.get_assignment(subject_in_class_id=subject_in_class.id)
        assignment.subject_in_class_id = subject_in_class.id
        assignment.data['class_id'] = subject_in_class.class_id
        assignment.data['section'] = subject_in_class.class_.section.identifier
        assignment.data['year'] = subject_in_class.class_.year.identifier
        assignment.data['subject_id'] = subject_in_class.subject.id
        assignment.data['subject'] = subject_in_class.subject.identifier
        assignment.data['hours_total'] = subject_in_class.hours_total
        assignment.data['max_hours_per_day'] = subject_in_class.max_hours_per_day
        assignment.data['persons'] = []
        # add all persons to the assignment
        for p in subject_in_class.persons:
            d = dict()
            d['person_id'] = p.id
            d['person'] = p.fullname
            assignment.data['persons'].append(d)
            # link the identifier to each person, for later use
            if p.id not in self._persons.keys():
                self._persons[p.id] = []
            self._persons[p.id].append(assignment)
        if subject_in_class.room is not None:
            assignment.data['room_id'] = subject_in_class.room.id
            assignment.data['room'] = subject_in_class.room.identifier
        else:
            assignment.data['room_id'] = None
            assignment.data['room'] = ''
        assignment.score = 0
        self.get_calendar(subject_in_class.class_id)

    def get_calendar(self, class_id=None) -> Calendar:
        if class_id in self._calendars.keys():
            return self._calendars[class_id]
        else:
            plan_id = db.query.get_plan_for_class(class_id)
            if plan_id:
                self._calendars[class_id] = Calendar(class_id=class_id)
                self._calendars[class_id].load(plan_id=plan_id)
                return self._calendars[class_id]

    def get_assignment_in_calendar(self, class_id, day, hour_ordinal):
        calendar = self.get_calendar(class_id=class_id)
        plan_day = calendar.day(day_id=day)
        if plan_day:
            if hour_ordinal in plan_day:
                return plan_day[hour_ordinal]
            else:
                return Calendar.UNAIVALABLE
        else:
            return Calendar.UNAIVALABLE

    def assign(self, subject_in_class_id: int, class_id: int, day: db.model.WeekDayEnum, hour_ordinal: int, score: int,
               constraint_scores: None):
        plan_day = self.get_calendar(class_id=class_id).day(day_id=day)
        plan_day[hour_ordinal] = self._assignments[subject_in_class_id]
        self._update_score(class_id=class_id, day=day, hour_ordinal=hour_ordinal, score=score,
                           constraint_scores=constraint_scores)

    def deassign(self, class_id: int, day: db.model.WeekDayEnum, hour_ordinal: int):
        plan_day = self.get_calendar(class_id=class_id).day(day_id=day)
        if type(plan_day[hour_ordinal]) == Assignment:
            plan_day[hour_ordinal] = Calendar.AVAILABLE
            self._update_score(class_id=class_id, day=day, hour_ordinal=hour_ordinal, score=0, constraint_scores=[])

    def _update_score(self, class_id, day, hour_ordinal, score, constraint_scores):
        if class_id not in self._scores.keys():
            self._scores[class_id] = {}
        self._scores[class_id][(day, hour_ordinal)] = (score, constraint_scores)

    def get_score(self, class_id: int, day: db.model.WeekDayEnum, hour_ordinal: int):
        if class_id not in self._scores.keys():
            return (0, None)
        if (day, hour_ordinal) not in self._scores[class_id]:
            return (0, None)
        return self._scores[class_id][(day, hour_ordinal)]

    def get_overall_score(self, class_id: int):
        score = 0
        if class_id not in self._scores.keys():
            return 0
        for (s, c) in self._scores[class_id]:
            score = score + self._scores[class_id][(s, c)][0]
        return score

    def get_calendar_ids(self):
        return self._calendars.keys()

    def write_calendars_to_csv(self, filename, filename_debug):
        with open(filename, 'w') as ff:
            for class_id in self.get_calendar_ids():
                class_ = db.query.get(db.model.Class, class_id)
                wstr = f'\nclasse {class_};lunedì;martedì;mercoledì;giovedì;venerdì;sabato;domenica;SCORE: {self.get_overall_score(class_id=class_id)}'
                for hour in range(1, 11):
                    wstr = wstr + f'\n{hour};'
                    for day in db.model.WeekDayEnum:
                        assignment = self.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour)
                        if assignment == Calendar.UNAIVALABLE:
                            continue
                        elif assignment == Calendar.AVAILABLE:
                            wstr = wstr + f'---;'
                        else:
                            subject = assignment.data['subject']
                            # (score, constraint_scores) = self.get_score(class_id=class_id, day=day, hour_ordinal=hour)
                            persons_list = [x['person'] for x in assignment.data['persons']]
                            persons_string = ",".join(persons_list)
                            wstr = wstr + f'{subject} ({persons_string});'
                ff.write(wstr + '\n')
            ff.write('\nDocenti\n')
            self.write_persons_to_csv(ff)

        if filename_debug is not None:
            with open(filename_debug, 'w') as ff:
                for class_id in self.get_calendar_ids():
                    class_ = db.query.get(db.model.Class, class_id)
                    wstr = f'\nclasse {class_};lunedì;martedì;mercoledì;giovedì;venerdì;sabato;domenica;SCORE: {self.get_overall_score(class_id=class_id)}'
                    for hour in range(1, 11):
                        wstr = wstr + f'\n{hour};'
                        for day in db.model.WeekDayEnum:
                            assignment = self.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour)
                            if assignment == Calendar.UNAIVALABLE:
                                continue
                            elif assignment == Calendar.AVAILABLE:
                                wstr = wstr + f'---;'
                            else:
                                subject = assignment.data['subject']
                                (score, constraint_scores) = self.get_score(class_id=class_id, day=day,
                                                                            hour_ordinal=hour)
                                persons_list = [x['person'] for x in assignment.data['persons']]
                                persons_string = ",".join(persons_list)
                                wstr = wstr + f'{subject} ({persons_string}) <{score}><{constraint_scores}>;'
                    ff.write(wstr + '\n')
                ff.write('\nDocenti\n')
                self.write_persons_to_csv(ff)

    def write_persons_to_csv(self, stream):
        persons = []
        for pid in self._persons.keys():
            person = db.query.get(db.model.Person, pid)
            persons.append(person.fullname)
        for person_fullname in sorted(persons, key=str.lower):
            wstr = str(person_fullname) + ';'
            for day in db.model.WeekDayEnum:
                for hour in range(1, 11):
                    for class_id in self.get_calendar_ids():
                        assignment = self.get_assignment_in_calendar(class_id=class_id, day=day, hour_ordinal=hour)
                        if assignment == Calendar.UNAIVALABLE or assignment == Calendar.AVAILABLE:
                            continue
                        else:
                            subject = assignment.data['subject']
                            persons_list = [x['person'] for x in assignment.data['persons']]
                            if person_fullname in persons_list:
                                year = str(assignment.data['year'])
                                section = str(assignment.data['section'])
                                wstr = wstr + f'{day.value} {hour} ( {year} {section});'
            stream.write(wstr + '\n')

    @property
    def constraints(self):
        return self._constraints

    @property
    def calendars(self):
        return self._calendars

    @property
    def assignments(self):
        return self._assignments

    @property
    def persons(self):
        return self._persons


class Engine:

    def __init__(self) -> None:
        self._struct = EngineSupport()
        self._closed = False
        self._suggest_continuing = False

    def load(self, school_year_id: int):
        rows = db.query.get_subjects_in_class_per_school_year(school_year_id=school_year_id)
        for row in rows:
            self.engine_support.load_assignment_from_subject_in_class(int(row))

    def clear_assignments(self):
        for calendar_id in self.engine_support.get_calendar_ids():
            for day in db.model.WeekDayEnum:
                for hour in range(1, 11):
                    self.engine_support.deassign(class_id=calendar_id, day=day, hour_ordinal=hour)

    def add_constraint(self, constraint):
        self.engine_support.constraints.add(constraint)

    def run(self):
        pass

    def write_calendars_to_csv(self, filename, filename_debug):
        self.engine_support.write_calendars_to_csv(filename=filename, filename_debug=filename_debug)

    @property
    def closed(self):
        return self._closed

    @property
    def engine_support(self):
        return self._struct
