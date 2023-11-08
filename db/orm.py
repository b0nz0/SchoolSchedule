from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
import model.entity

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    start_datetime:Mapped[Optional[datetime]]
    log_user: Mapped[Optional[str]]

class School(Base):
    __tablename__ = "school"
    name: Mapped[str] = mapped_column(String(30))
    schoolyears: Mapped[List["SchoolYear"]] = relationship(
                 back_populates="school", cascade="all, delete-orphan"
                 )
    
    def to_entity(self):
        entity = model.entity.School()
        entity.object_id = self.id
        entity.start_date = self.start_datetime
        entity.log_user = self.log_user
        entity.name = self.name
        return entity        

    def from_entity(self, entity: model.entity.School):
        if entity.object_id == 0:
            self.id = None
        else:
            self.id = entity.object_id
        self.start_datetime = entity.start_date
        self.log_user = entity.log_user
        self.name = entity.name
        return self

    def __repr__(self) -> str:
        return f"school(id={self.id!r}, name={self.name!r})"

class SchoolYear(Base):
    __tablename__ = "school_year"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="schoolyears")

    def to_entity(self):
        entity = model.entity.SchoolYear()
        entity.object_id = self.id
        entity.start_date = self.start_datetime
        entity.log_user = self.log_user
        entity.identifier = self.identifier
        entity.school = self.school
        return entity

    def from_entity(self, entity: model.entity.SchoolYear):
        if entity.object_id == 0:
            self.id = None
        else:
            self.id = entity.object_id
        self.start_datetime = entity.start_date
        self.log_user = entity.log_user
        self.identifier = entity.identifier
        self.school = entity.school
        return self

    def __repr__(self) -> str:
        return f"schoolyear(id={self.id!r}, identifier={self.identifier!r}, school={self.school.name})"