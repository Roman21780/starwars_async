from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    birth_year = Column(String(10))
    eye_color = Column(String(20))
    films = Column(Text)  # названия фильмов через запятую
    gender = Column(String(10))
    hair_color = Column(String(20))
    height = Column(String(10))
    homeworld = Column(String(255))
    mass = Column(String(10))
    name = Column(String(100))
    skin_color = Column(String(20))
    species = Column(Text)  # названия типов через запятую
    starships = Column(Text)  # названия кораблей через запятую
    vehicles = Column(Text)  # названия транспорта через запятую
