import enum
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    start_datetime:Mapped[Optional[datetime]]
    log_user: Mapped[Optional[str]]

class School(Base):
    __tablename__ = "school"
    name: Mapped[str] = mapped_column(String(30))
    schoolyears: Mapped[List["SchoolYear"]] = relationship(
                 back_populates="school", cascade="all, delete-orphan")
    years: Mapped[List["Year"]] = relationship(
                 back_populates="school", cascade="all, delete-orphan")
    sections: Mapped[List["Section"]] = relationship(
                 back_populates="school", cascade="all, delete-orphan")
    rooms: Mapped[List["Room"]] = relationship(
                 back_populates="school", cascade="all, delete-orphan")
    persons: Mapped[List["Person"]] = relationship(
                 back_populates="school", cascade="all, delete-orphan")
    subjects: Mapped[List["Subject"]] = relationship(
                 back_populates="school", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"school(id={self.id!r}, name={self.name!r})"

class SchoolYear(Base):
    __tablename__ = "school_year"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="schoolyears")
    classes: Mapped[List["Class"]] = relationship(
        back_populates="school_year", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"schoolyear(id={self.id!r}, identifier={self.identifier!r}, school={self.school.name!r})"
    
class Year(Base):
    __tablename__ = "year"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="years")
    classes: Mapped[List["Class"]] = relationship(
        back_populates="year", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"year(id={self.id!r}, identifier={self.identifier!r}, school={self.school.name})"
    
class Section(Base):
    __tablename__ = "section"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="sections")
    classes: Mapped[List["Class"]] = relationship(
        back_populates="section", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"year(id={self.id!r}, identifier={self.identifier!r}, school={self.school.name})"
    
class Class(Base):
    __tablename__ = "class_"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_year_id: Mapped[int] = mapped_column(ForeignKey("school_year.id"))
    school_year: Mapped["SchoolYear"] = relationship(back_populates="classes")
    year_id: Mapped[int] = mapped_column(ForeignKey("year.id"))
    year: Mapped["Year"] = relationship(back_populates="classes", lazy="joined")
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id"))
    section: Mapped["Section"] = relationship(back_populates="classes", lazy="joined")

    def __repr__(self) -> str:
        return f"class {self.year.identifier} {self.section.identifier} {self.school_year.identifier}"
    
class RoomEnum(enum.Enum):
    AULA = "aula"
    PALESTRA = "palestra"
    LABORATORIO = "laboratorio"
    ALTRO = "altro"
    
class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    room_type: Mapped[RoomEnum]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="rooms")
    
    def __repr__(self) -> str:
        return f"{self.identifier} ({self.room_type})"

class PersonEnum(enum.Enum):
    DOCENTE = "docente"
    COLLABORATORE = "collaboratore"
    LETTORE = "lettore"
    ALTRO = "altro"
    
class Person(Base):
    __tablename__ = "person"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str]
    title: Mapped[str]
    is_impersonal: Mapped[bool]
    person_type: Mapped[RoomEnum]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="persons")
    
    def __repr__(self) -> str:
        return f"{self.title} {self.firstname} {self.lastname}"
    
class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="subjects")

    def __repr__(self) -> str:
        return f"{self.identifier}"

class SubjectInClass(Base):
    __tablename__ = "subject_in_class"
    id: Mapped[int] = mapped_column(primary_key=True)
    hours_total: Mapped[int]
    max_hours_per_day: Mapped[int]
    
    class_id: Mapped[int] = mapped_column(ForeignKey("class_.id"))
    class_: Mapped["Class"] = relationship(lazy="joined")  
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    subject: Mapped["Subject"] = relationship(lazy="joined")
    
    def __repr__(self) -> str:
        return f"{self.subject.identifier} in {self.class_.year.identifier} {self.class_.section.identifier}"