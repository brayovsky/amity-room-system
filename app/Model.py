from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Rooms(Base):
    __tablename__ = 'rooms'
    room_name = Column(String(250), primary_key=True)
    room_type = Column(String(250), nullable=False)


class People(Base):
    __tablename__ = 'people'
    person_name = Column(String(250), primary_key=True)
    person_type = Column(String(250), nullable=False)
    wants_accommodation = Column(Boolean, default=False)


class Allocations(Base):
    __tablename__ = 'allocations'
    id = Column(Integer, primary_key=True)
    person_name = Column(String(250), ForeignKey('people.person_name'))
    room_name = Column(String(250), ForeignKey('rooms.room_name'))
    room = relationship(Rooms)
    person = relationship(People)
