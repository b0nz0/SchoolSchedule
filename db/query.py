import traceback
from typing import List
import psycopg
import db.connection
from sqlalchemy import select
import db.model

def get_schools() -> List[db.model.School]:
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.School).order_by(db.model.School.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_schoolyears(school_id) -> List[db.model.SchoolYear]:
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.SchoolYear).\
                where(db.model.SchoolYear.school_id == school_id).\
                    order_by(db.model.SchoolYear.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_years(school_id) -> List[db.model.Year]:
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.Year).\
                where(db.model.Year.school_id == school_id).\
                    order_by(db.model.Year.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_sections(school_id) -> List[db.model.Section]:
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.Section).\
                where(db.model.Section.school_id == school_id).\
                    order_by(db.model.Section.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_classes(schoolyear_id) -> List[db.model.Class]:
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.Class).\
                where(db.model.Class.school_year_id == schoolyear_id).\
                    order_by(db.model.Class.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_rooms(school_id) -> List[db.model.Room]:
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.Room).\
                where(db.model.Room.school_id == school_id).\
                    order_by(db.model.Room.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_plans(school_id) -> List[db.model.Plan]:
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.Plan).\
                where(db.model.Plan.school_id == school_id).\
                    order_by(db.model.Plan.id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_school(school: db.model.School):
    if school.id != None and school.id != 0:
        return (get(db.model.School, school.id))
    elif school.name != None and school.name != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.School).\
                    where(db.model.School.name == school.name)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False

def get_schoolyear(schoolyear: db.model.SchoolYear):
    if schoolyear.id != None and schoolyear.id != 0:
        return get(db.model.SchoolYear, schoolyear.id)
    elif schoolyear.identifier != None and schoolyear.identifier != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.SchoolYear).\
                    where(db.model.SchoolYear.identifier == schoolyear.identifier)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False

def get_year(year: db.model.Year):
    if year.id != None and year.id != 0:
        return get(db.model.Year, year.id)
    elif year.identifier != None and year.identifier != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.Year).\
                    where(db.model.Year.identifier == year.identifier)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False

def get_section(section: db.model.Section):
    if section.id != None and section.id != 0:
        return get(db.model.Section, section.id)
    elif section.identifier != None and section.identifier != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.Section).\
                    where(db.model.Section.identifier == section.identifier)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    else:
        return False

def get_class(classe: db.model.Class):
    if classe.id != None and classe.id != 0:
        return get(db.model.Section, classe.id)
    elif classe.school_year_id != None and classe.school_year_id != 0 and \
            classe.year_id != None and classe.year_id != 0 and \
            classe.section_id != None and classe.section_id != 0:
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.Class).\
                    where(db.model.Class.school_year_id == classe.school_year_id, 
                        db.model.Class.year_id == classe.year_id, 
                        db.model.Class.section_id == classe.section_id)
                return session.execute(stmt).first()
        except (Exception) as error:
            traceback.print_exc()
    elif classe.school_year != None and \
            classe.year != None and \
            classe.section != None:
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.Class).\
                    where(db.model.Class.school_year == classe.school_year, 
                        db.model.Class.year == classe.year, 
                        db.model.Class.section == classe.section)
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
            session.add(entity)
            session.commit()
            return entity
    except (Exception) as error:
        traceback.print_exc()

def get_plan(id = 0, name = None):
    try:
        with db.connection.active_session() as session:
            if name:
                stmt = select(db.model.Plan).\
                    where(db.model.Plan.identifier == name)
                plan = session.execute(stmt).scalar()
            else:
                plan = get(db.model.Plan, id=id)
            if not plan:
                    return None
            id = plan.id
            
            stmt = select(db.model.DailyHour).\
                    where(db.model.DailyHour.plan_id == id).order_by(db.model.DailyHour.ordinal)
            daily_hours = session.execute(stmt).scalars().all()    
            
            days = {}
            days[db.model.WeekDayEnum.MONDAY] = []
            days[db.model.WeekDayEnum.TUESDAY] = []
            days[db.model.WeekDayEnum.WEDNESDAY] = []
            days[db.model.WeekDayEnum.THURSDAY] = []
            days[db.model.WeekDayEnum.FRIDAY] = []
            days[db.model.WeekDayEnum.SATURDAY] = []
            days[db.model.WeekDayEnum.SUNDAY] = []
            for daily_hour in daily_hours:
                # newday = list([h for h in days[daily_hour.week_day] if h.start < daily_hour.hour.start])
                # newday.append(daily_hour.hour)
                # rest = [h for h in days[daily_hour.week_day] if h.start > daily_hour.hour.start]
                # if len(rest) > 0:
                #     newday.append(rest)
                # days[daily_hour.week_day] = newday
                days[daily_hour.week_day].append(daily_hour.hour)
            return days

    except (Exception) as error:
        traceback.print_exc()

def get_classes_in_plan(id: int):
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.ClassPlan).\
                    where(db.model.ClassPlan.plan_id == id)
            return session.execute(stmt).scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def get_subjects_in_class(id: int):
    try:
        with db.connection.active_session() as session:
            stmt = select(db.model.SubjectInClass).\
                    where(db.model.SubjectInClass.class_id == id)
            return session.execute(stmt).unique().scalars().all()
    except (Exception) as error:
        traceback.print_exc()

def dump_school_year(id: int) -> str:
    try:
        out = str()
        with db.connection.active_session() as session:
            schoolyear = get(db.model.SchoolYear, id=id)
            out = out + f'Anno scolastico {schoolyear.identifier}\nClassi:'
            session.add(schoolyear)
            classes = get_classes(id)
            for classe in classes:
                out = out + dump_class(classe.id)
                for subject_in_class in get_subjects_in_class(classe.id):
                    out = out + dump_subject_in_class(subject_in_class.id)
        return out    
    except (Exception) as error:
        traceback.print_exc()
    
def dump_class(id: int) -> str:
    try:
        out = str()
        with db.connection.active_session() as session:
            class_ = get(db.model.Class, id=id)
            session.add(class_)
            out = out + f'Classe {class_.year.identifier} {class_.section.identifier}\n'
            return out
            
    except (Exception) as error:
        traceback.print_exc()

def dump_subject_in_class(id: int) -> str:
    try:
        out = str()
        with db.connection.active_session() as session:
            sic = get(db.model.SubjectInClass, id=id)
            session.add(sic)
            out = out + f'{sic.subject.identifier} ('
            out = out + ','.join([person.fullname for person in sic.persons])
            out = out + ')\n'
            return out
            
    except (Exception) as error:
        traceback.print_exc()
        