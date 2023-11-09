from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
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
    __tablename__ = "class"
    id: Mapped[int] = mapped_column(primary_key=True)
    school_year_id: Mapped[int] = mapped_column(ForeignKey("school_year.id"))
    school_year: Mapped["SchoolYear"] = relationship(back_populates="classes")
    year_id: Mapped[int] = mapped_column(ForeignKey("year.id"))
    year: Mapped["Year"] = relationship(back_populates="classes")
    section_id: Mapped[int] = mapped_column(ForeignKey("section.id"))
    section: Mapped["Section"] = relationship(back_populates="classes")

    def __repr__(self) -> str:
        return f"class {self.year.identifier} {self.section.identifier} {self.school_year.identifier}"
    
