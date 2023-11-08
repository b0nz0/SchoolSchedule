import traceback
from typing import List
import psycopg
import db.connection
import db.orm
from datetime import datetime
import model.entity
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_schools() -> List[model.entity.School]:
    try:
        with Session(db.connection.active_engine) as session:
            stmt = select(db.orm.School).order_by(db.orm.School.id)
            schools = []
            for schoolrow in session.scalars(stmt):
                schools.append(schoolrow.to_entity())
            return schools
    except (Exception) as error:
        traceback.print_exc()

def get_school(id: int) -> db.orm.School:
    try:
        with Session(db.connection.active_engine) as session:
            return session.get(db.orm.School, id)
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

def write_school(school:model.entity.School, log_user: str) -> model.entity.School:
    try:
        with Session(db.connection.active_engine) as session:
            if school.object_id == None or school.object_id == 0:
                schoolrow = db.orm.School().from_entity(school)
                session.add(schoolrow)
            else:
                schoolrow = session.get(db.orm.School, school.object_id)
                schoolrow.from_entity(school)
            schoolrow.log_user = log_user
            session.commit()
            return schoolrow.to_entity()
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

