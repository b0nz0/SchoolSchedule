import traceback
import logging
from typing import List
import psycopg
import sqlalchemy

import db.connection
from sqlalchemy import select
from db.model import *
import engine.constraint, engine.struct


def get_schools() -> List[School]:
    try:
        with db.connection.active_session() as session:
            stmt = select(School).order_by(School.name)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_schoolyears(school_id) -> List[SchoolYear]:
    try:
        with db.connection.active_session() as session:
            stmt = select(SchoolYear). \
                where(SchoolYear.school_id == school_id). \
                order_by(SchoolYear.identifier)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_years(school_id) -> List[Year]:
    try:
        with db.connection.active_session() as session:
            stmt = select(Year). \
                where(Year.school_id == school_id). \
                order_by(Year.identifier)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_sections(school_id) -> List[Section]:
    try:
        with db.connection.active_session() as session:
            stmt = select(Section). \
                where(Section.school_id == school_id). \
                order_by(Section.identifier)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_classes(schoolyear_id) -> List[Class]:
    try:
        with db.connection.active_session() as session:
            stmt = select(Class). \
                where(Class.school_year_id == schoolyear_id). \
                order_by(Class.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_rooms(school_id) -> List[Room]:
    try:
        with db.connection.active_session() as session:
            stmt = select(Room). \
                where(Room.school_id == school_id). \
                order_by(Room.identifier)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_subjects(school_id) -> List[Subject]:
    try:
        with db.connection.active_session() as session:
            stmt = select(Subject). \
                where(Subject.school_id == school_id). \
                order_by(Subject.identifier)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_persons(school_id) -> List[Person]:
    try:
        with db.connection.active_session() as session:
            stmt = select(Person). \
                where(Person.school_id == school_id). \
                order_by(Person.fullname)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_plans(school_id) -> List[Plan]:
    try:
        with db.connection.active_session() as session:
            stmt = select(Plan). \
                where(Plan.school_id == school_id). \
                order_by(Plan.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_school(school: School):
    if school.id is not None and school.id != 0:
        return get(School, school.id)
    elif school.name != None and school.name != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(School). \
                    where(School.name == school.name)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False


def get_schoolyear(schoolyear: SchoolYear):
    if schoolyear.id is not None and schoolyear.id != 0:
        return get(SchoolYear, schoolyear.id)
    elif schoolyear.identifier is not None and schoolyear.identifier != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(SchoolYear). \
                    where(SchoolYear.identifier == schoolyear.identifier)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False


def get_year(year: Year):
    if year.id is not None and year.id != 0:
        return get(Year, year.id)
    elif year.identifier is not None and year.identifier != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(Year). \
                    where(Year.identifier == year.identifier)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False


def get_section(section: Section):
    if section.id is not None and section.id != 0:
        return get(Section, section.id)
    elif section.identifier is not None and section.identifier != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(Section). \
                    where(Section.identifier == section.identifier)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False

def get_room(room: Room):
    if room.id is not None and room.id != 0:
        return get(Room, room.id)
    elif room.identifier is not None and room.identifier != '' and room.school_id is not None:
        try:
            with db.connection.active_session() as session:
                stmt = select(Room). \
                    where(Room.identifier == room.identifier, Room.room_type == room.room_type,
                          Room.school_id == room.school_id)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False

def get_person(person: Person):
    if person.id is not None and person.id != 0:
        return get(Person, person.id)
    elif person.fullname is not None and person.fullname != '' and person.school_id is not None:
        try:
            with db.connection.active_session() as session:
                stmt = select(Person). \
                    where(Person.fullname == person.fullname, Person.person_type == person.person_type,
                          Person.school_id == person.school_id)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False


def get_subject(subject: Subject):
    if subject.id is not None and subject.id != 0:
        return get(Subject, subject.id)
    elif subject.identifier is not None and subject.identifier != '' and subject.school_id is not None:
        try:
            with db.connection.active_session() as session:
                stmt = select(Subject). \
                    where(Subject.identifier == subject.identifier, Subject.school_id == subject.school_id)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False


def get_class(classe: Class):
    if classe.id is not None and classe.id != 0:
        return get(Section, classe.id)
    elif classe.school_year_id is not None and classe.school_year_id != 0 and \
            classe.year_id is not None and classe.year_id != 0 and \
            classe.section_id is not None and classe.section_id != 0:
        try:
            with db.connection.active_session() as session:
                stmt = select(Class). \
                    where(Class.school_year_id == classe.school_year_id,
                          Class.year_id == classe.year_id,
                          Class.section_id == classe.section_id)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    elif classe.school_year is not None and \
            classe.year is not None and \
            classe.section is not None:
        try:
            with db.connection.active_session() as session:
                stmt = select(Class). \
                    where(Class.school_year == classe.school_year,
                          Class.year == classe.year,
                          Class.section == classe.section)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False


def get(entityclass, id: int):
    try:
        with db.connection.active_session() as session:
            return session.get(entityclass, id)
    except (Exception) as error:
        traceback.print_exc()


def delete(entityclass, id: int):
    try:
        with db.connection.active_session() as session:
            session.delete(session.get(entityclass, id))
            session.commit()
    except (Exception) as error:
        traceback.print_exc()


def save(entity, log_user="-"):
    try:
        with db.connection.active_session() as session:
            entity.log_user = log_user
            session.merge(entity)
            session.commit()
            return entity
    except (Exception) as error:
        traceback.print_exc()


def get_plan(plan_id=0, name=None):
    try:
        with db.connection.active_session() as session:
            if name:
                stmt = select(Plan). \
                    where(Plan.identifier == name)
                plan = session.execute(stmt).scalar()
            else:
                plan = get(Plan, id=plan_id)
            if not plan:
                return None
            plan_id = plan.id

            stmt = select(DailyHour). \
                where(DailyHour.plan_id == plan_id).order_by(DailyHour.ordinal)
            daily_hours = session.execute(stmt).scalars().all()

            days = {WeekDayEnum.MONDAY: [], WeekDayEnum.TUESDAY: [], WeekDayEnum.WEDNESDAY: [],
                    WeekDayEnum.THURSDAY: [], WeekDayEnum.FRIDAY: [], WeekDayEnum.SATURDAY: [], WeekDayEnum.SUNDAY: []}
            for daily_hour in daily_hours:
                days[daily_hour.week_day].append(daily_hour)
            return days

    except (Exception) as error:
        traceback.print_exc()


def get_classes_in_plan(plan_id: int):
    try:
        with db.connection.active_session() as session:
            stmt = select(ClassPlan). \
                where(ClassPlan.plan_id == plan_id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_plan_for_class(class_id: int):
    try:
        with db.connection.active_session() as session:
            stmt = select(ClassPlan.plan_id). \
                where(ClassPlan.class_id == class_id)
            return session.execute(stmt).scalar_one_or_none()
    except (Exception) as error:
        traceback.print_exc()

def delete_plan_for_class(class_id: int):
    try:
        with db.connection.active_session() as session:
            stmt = sqlalchemy.delete(ClassPlan). \
                where(ClassPlan.class_id == class_id)
            session.execute(stmt)
            session.commit()
    except (Exception) as error:
        traceback.print_exc()


def get_subject_in_class(subject_in_class: SubjectInClass):
    try:
        with db.connection.active_session() as session:
            stmt = select(SubjectInClass). \
                where(SubjectInClass.class_id == subject_in_class.class_id,
                      SubjectInClass.subject_id == subject_in_class.subject_id)
            return session.execute(stmt).unique().scalar_one_or_none()
    except (Exception) as error:
        traceback.print_exc()

def get_subjects_in_class(class_id: int):
    try:
        with db.connection.active_session() as session:
            stmt = select(SubjectInClass). \
                where(SubjectInClass.class_id == class_id)
            return session.execute(stmt).unique().scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_subjects_in_class_per_school_year(school_year_id: int, person_id=None):
    try:
        with db.connection.active_session() as session:
            if person_id:
                stmt = select(PersonToSubjectInClassAssociation.subject_in_class_id). \
                    join(SubjectInClass).join(Class). \
                    where(PersonToSubjectInClassAssociation.person_id == person_id,
                          Class.school_year_id == school_year_id)
            else:
                stmt = select(PersonToSubjectInClassAssociation.subject_in_class_id). \
                    join(SubjectInClass).join(Class). \
                    where(Class.school_year_id == school_year_id)
            return session.execute(stmt).unique().scalars().all()
    except (Exception) as error:
        traceback.print_exc()


def get_constraint(classname: str, id: int):
    c = db.query.get(Constraint, id)
    class_obj = getattr(engine.constraint, classname)
    retc = class_obj()
    retc.from_model(c)
    return retc


def get_constraints(school_year_id: int) -> List[engine.struct.Constraint]:
    try:
        with db.connection.active_session() as session:
            if school_year_id is not None:
                stmt = select(Constraint).where(Constraint.school_year_id == school_year_id).order_by(Constraint.id)
            else:
                stmt = select(Constraint).order_by(Constraint.id)
            rets = []
            for c in session.execute(stmt).scalars().all():
                for ckind in engine.struct.Constraint.REGISTERED_CONSTRAINTS:
                    if c.kind == ckind['shortname']:
                        class_obj = getattr(engine.constraint, ckind['classname'])
                        retc = class_obj()
                        break
                retc.from_model(c)
                rets.append(retc)
            return rets
    except (Exception) as error:
        traceback.print_exc()


def dump_school_year(id: int) -> str:
    try:
        out = str()
        with db.connection.active_session() as session:
            schoolyear = get(SchoolYear, id=id)
            out = out + f'Anno scolastico {schoolyear.identifier}\nClassi:'
            session.add(schoolyear)
            classes = get_classes(id)
            for classe in classes:
                out = out + dump_class(classe.id)
                for subject_in_class in get_subjects_in_class(classe.id):
                    out = out + dump_subject_in_class(subject_in_class.id)
                out = out + '\nTimetable:\n'
                stmt = select(ClassPlan). \
                    where(ClassPlan.class_id == classe.id)
                classplan = session.execute(stmt).scalar()
                plan = get_plan(classplan.plan_id)
                for day in [WeekDayEnum.MONDAY,
                            WeekDayEnum.TUESDAY,
                            WeekDayEnum.WEDNESDAY,
                            WeekDayEnum.THURSDAY,
                            WeekDayEnum.FRIDAY,
                            WeekDayEnum.SATURDAY,
                            WeekDayEnum.SUNDAY,
                            ]:
                    out = out + str(day.value) + ": \t"
                    for daily_hour in plan[day]:
                        out = out + daily_hour.hour.start.strftime('%H:%M') + "-" + daily_hour.hour.get_end().strftime(
                            '%H:%M') + " ; "
                    out = out + "\n"
        return out
    except (Exception) as error:
        traceback.print_exc()


def dump_class(id: int) -> str:
    try:
        out = str()
        with db.connection.active_session() as session:
            class_ = get(Class, id=id)
            session.add(class_)
            out = out + f'\nClasse {class_.year.identifier} {class_.section.identifier}\n'
            return out

    except (Exception) as error:
        traceback.print_exc()


def dump_subject_in_class(id: int) -> str:
    try:
        out = str()
        with db.connection.active_session() as session:
            sic = get(SubjectInClass, id=id)
            session.add(sic)
            out = out + f'{sic.subject.identifier} ('
            out = out + ','.join([person.fullname for person in sic.persons])
            out = out + f') {sic.hours_total} ore\n'
            return out

    except (Exception) as error:
        traceback.print_exc()
