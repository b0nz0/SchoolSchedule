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

def get(entityclass, id):
    try:
        with db.connection.active_session() as session:
            return session.get(entityclass, id)
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

def delete(entityclass, id):
    try:
        with db.connection.active_session() as session:
            session.delete(session.get(entityclass, id))
            session.commit()
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

def save(entity, log_user: str):
    try:
        with db.connection.active_session() as session:
            entity.log_user = log_user
            session.add(entity)
            session.commit()
            return entity
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

