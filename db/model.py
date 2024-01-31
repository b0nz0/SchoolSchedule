import enum
from datetime import datetime, time, timedelta
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    start_datetime: Mapped[Optional[datetime]] = mapped_column(default=datetime.now, onupdate=datetime.now)
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
    hours: Mapped[List["Hour"]] = relationship(
        back_populates="school", cascade="all, delete-orphan")
    plans: Mapped[List["Plan"]] = relationship(
        back_populates="school", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"school(id={self.id!r}, name={self.name!r})"


class SchoolYear(Base):
    __tablename__ = "school_year"

    identifier: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="schoolyears")
    classes: Mapped[List["Class"]] = relationship(
        back_populates="school_year", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"schoolyear(id={self.id!r}, identifier={self.identifier!r}, school={self.school.name!r})"


class Year(Base):
    __tablename__ = "year"

    identifier: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="years")
    classes: Mapped[List["Class"]] = relationship(
        back_populates="year", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"year(id={self.id!r}, identifier={self.identifier!r}, school={self.school.name})"


class Section(Base):
    __tablename__ = "section"

    identifier: Mapped[str]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="sections")
    classes: Mapped[List["Class"]] = relationship(
        back_populates="section", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"year(id={self.id!r}, identifier={self.identifier!r}, school={self.school.name})"


class Class(Base):
    __tablename__ = "class_"

    school_year_id: Mapped[int] = mapped_column(ForeignKey("school_year.id"))
    school_year: Mapped["SchoolYear"] = relationship(back_populates="classes", lazy="joined")
    year_id: Mapped[int] = mapped_column(ForeignKey("year.id"))
    year: Mapped["Year"] = relationship(back_populates="classes", lazy="joined")
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id"))
    section: Mapped["Section"] = relationship(back_populates="classes", lazy="joined")

    def long_repr(self) -> str:
        return f'{self.year.identifier} {self.section.identifier} {self.school_year.identifier}'

    def __repr__(self) -> str:
        return f'{self.year.identifier} {self.section.identifier}'


class RoomEnum(enum.Enum):
    AULA = "aula"
    PALESTRA = "palestra"
    LABORATORIO = "laboratorio"
    ALTRO = "altro"


class Room(Base):
    __tablename__ = "room"

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

    fullname: Mapped[str]
    title: Mapped[str]
    is_impersonal: Mapped[bool]
    person_type: Mapped[PersonEnum]
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="persons")

    #    subjects_in_class: Mapped[List["SubjectInClass"]] = relationship(secondary="person_to_subject_in_class", lazy="joined")

    def __repr__(self) -> str:
        return f"{self.title} {self.fullname}"


class Subject(Base):
    __tablename__ = "subject"

    identifier: Mapped[str]
    default_hours: Mapped[int]
    preferred_consecutive_hours: Mapped[int]

    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="subjects")

    def __repr__(self) -> str:
        return f"{self.identifier}"


class SubjectInClass(Base):
    __tablename__ = "subject_in_class"

    hours_total: Mapped[int]
    max_hours_per_day: Mapped[int]

    class_id: Mapped[int] = mapped_column(ForeignKey("class_.id"))
    class_: Mapped["Class"] = relationship(lazy="joined")
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    subject: Mapped["Subject"] = relationship(lazy="joined")
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room: Mapped[Optional["Room"]] = relationship(lazy="joined")

    persons: Mapped[List["Person"]] = relationship(secondary="person_to_subject_in_class", lazy="joined")

    # room: Mapped["Room"] = relationship()

    def __repr__(self) -> str:
        return f"{self.subject.identifier} in {self.class_.year.identifier} {self.class_.section.identifier}"


class PersonToSubjectInClassAssociation(Base):
    __tablename__ = "person_to_subject_in_class"

    subject_in_class_id: Mapped[int] = mapped_column(ForeignKey("subject_in_class.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))

    def __repr__(self) -> str:
        return f"M-N relationship"


class Hour(Base):
    __tablename__ = "hour"

    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="hours")

    start: Mapped[time]
    minutes: Mapped[int]

    def get_end(self) -> time:
        dt = datetime(1970, 1, 1, hour=self.start.hour, minute=self.start.minute)
        tt = dt + timedelta(minutes=self.minutes)
        return time(hour=tt.hour, minute=tt.minute)

    def __repr__(self) -> str:
        return f"{self.start} ({self.minutes}m)"


class Plan(Base):
    __tablename__ = "plan"

    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"))
    school: Mapped["School"] = relationship(back_populates="plans")

    identifier: Mapped[str]
    daily_hours: Mapped[List["DailyHour"]] = relationship(
        back_populates="plan", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.identifier}"


class WeekDayEnum(enum.Enum):
    MONDAY = "lunedì"
    TUESDAY = "martedì"
    WEDNESDAY = "mercoledì"
    THURSDAY = "giovedì"
    FRIDAY = "venerdì"
    SATURDAY = "sabato"
    SUNDAY = "domenica"


class DailyHour(Base):
    __tablename__ = "daily_hour"

    plan_id: Mapped[int] = mapped_column(ForeignKey("plan.id"))
    plan: Mapped["Plan"] = relationship(back_populates="daily_hours")

    week_day: Mapped[WeekDayEnum]
    ordinal: Mapped[int]
    hour_id: Mapped[int] = mapped_column(ForeignKey("hour.id"))
    hour: Mapped["Hour"] = relationship(lazy="joined")

    def __repr__(self) -> str:
        return f"{self.week_day}: {self.hour}"


class ClassPlan(Base):
    __tablename__ = "class_plan"

    plan_id: Mapped[int] = mapped_column(ForeignKey("plan.id"))
    plan: Mapped["Plan"] = relationship(lazy="joined")

    class_id: Mapped[int] = mapped_column(ForeignKey("class_.id"))
    class_: Mapped["Class"] = relationship(lazy="joined")

    def __repr__(self) -> str:
        return f"{self.class_}-{self.plan}"


class Constraint(Base):
    __tablename__ = "constraint"

    school_year_id: Mapped[int] = mapped_column(ForeignKey("school_year.id"))
    school_year: Mapped["SchoolYear"] = relationship()

    engine_id: Mapped[int]

    identifier: Mapped[str]
    kind: Mapped[str]
    score: Mapped[int]
    configuration: Mapped[str]

    def __repr__(self) -> str:
        return f"{self.identifier} of kind {self.kind}"
