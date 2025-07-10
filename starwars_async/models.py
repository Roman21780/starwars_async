from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    birth_year = Column(String(20), nullable=True)
    eye_color = Column(String(20), nullable=True)
    films = Column(Text, nullable=True)
    gender = Column(String(20), nullable=True)
    hair_color = Column(String(50), nullable=True)
    height = Column(String(10), nullable=True)
    homeworld = Column(String(255), nullable=True)
    mass = Column(String(20), nullable=True)
    name = Column(String(100), nullable=False)
    skin_color = Column(String(50), nullable=True)
    species = Column(Text, nullable=True)
    starships = Column(Text, nullable=True)
    vehicles = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Character(id={self.id}, name={self.name})>"


class Starship(Base):
    __tablename__ = 'starships'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    model = Column(String(100), nullable=True)
    manufacturer = Column(String(255), nullable=True)
    cost_in_credits = Column(String(50), nullable=True)
    length = Column(String(50), nullable=True)
    crew = Column(String(50), nullable=True)
    passengers = Column(String(50), nullable=True)
    cargo_capacity = Column(String(50), nullable=True)
    consumables = Column(String(50), nullable=True)
    hyperdrive_rating = Column(String(50), nullable=True)
    starship_class = Column(String(100), nullable=True)
    films = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Starship(id={self.id}, name={self.name})>"


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    model = Column(String(100), nullable=True)
    manufacturer = Column(String(255), nullable=True)
    cost_in_credits = Column(String(50), nullable=True)
    length = Column(String(50), nullable=True)
    crew = Column(String(50), nullable=True)
    passengers = Column(String(50), nullable=True)
    cargo_capacity = Column(String(50), nullable=True)
    consumables = Column(String(50), nullable=True)
    vehicle_class = Column(String(100), nullable=True)
    films = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Vehicle(id={self.id}, name={self.name})>"


class Planet(Base):
    __tablename__ = 'planets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    diameter = Column(String(50), nullable=True)
    rotation_period = Column(String(50), nullable=True)
    orbital_period = Column(String(50), nullable=True)
    gravity = Column(String(50), nullable=True)
    population = Column(String(50), nullable=True)
    climate = Column(String(100), nullable=True)
    terrain = Column(String(100), nullable=True)
    surface_water = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Planet(id={self.id}, name={self.name})>"