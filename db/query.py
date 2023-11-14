import traceback
from typing import List
import psycopg
import db.connection
from sqlalchemy import select

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

def get_school(school: db.model.School):
    if school.id != None and school.id != 0:
        return (get(db.model.School, school.id))
    elif school.name != None and school.name != '':
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.School).\
                    where(db.model.School.name == school.name)
                return session.execute(stmt).first()
        except (Exception, psycopg.DatabaseError) as error:
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
        except (Exception, psycopg.DatabaseError) as error:
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
        except (Exception, psycopg.DatabaseError) as error:
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
        except (Exception, psycopg.DatabaseError) as error:
            traceback.print_exc()
    else:
        return False

def get_class(class0: db.model.Class):
    if class0.id != None and class0.id != 0:
        return get(db.model.Section, class0.id)
    elif class0.school_year_id != None and class0.school_year_id != 0 and \
            class0.year_id != None and class0.year_id != 0 and \
            class0.section_id != None and class0.section_id != 0:
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.Class).\
                    where(db.model.Class.school_year_id == class0.school_year_id and \
                        db.model.Class.year_id == class0.year_id and
                        db.model.Class.section_id == class0.section_id)
                return session.execute(stmt).first()
        except (Exception, psycopg.DatabaseError) as error:
            traceback.print_exc()
    elif class0.school_year != None and \
            class0.year != None and \
            class0.section != None:
        try:
            with db.connection.active_session() as session:
                stmt = select(db.model.Class).\
                    where(db.model.Class.school_year == class0.school_year and \
                        db.model.Class.year == class0.year and
                        db.model.Class.section == class0.section)
                return session.execute(stmt).first()
        except (Exception, psycopg.DatabaseError) as error:
            traceback.print_exc()
    else:
        return False

def get(entityclass, id: int):
    try:
        with db.connection.active_session() as session:
            return session.get(entityclass, id)
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

def delete(entityclass, id: int):
    try:
        with db.connection.active_session() as session:
            session.delete(session.get(entityclass, id))
            session.commit()
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

def save(entity, log_user="-"):
    try:
        with db.connection.active_session() as session:
            entity.log_user = log_user
            session.add(entity)
            session.commit()
            return entity
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

