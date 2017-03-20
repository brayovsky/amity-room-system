from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Rooms(Base):
    __tablename__ = 'rooms'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    room_name = Column(String(250), primary_key=True)
    room_type = Column(String(1), nullable=False)


class People(Base):
    __tablename__ = 'people'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    # id = Column(Integer, primary_key=True)
    person_name = Column(String(250), primary_key=True)
    person_type = Column(String(1), nullable=False)
    office = Column(String(250), ForeignKey('rooms.room_name'), nullable=True)
    living_space = Column(String(250), ForeignKey('rooms.room_name'), nullable=True)
    room = relationship(Rooms)
