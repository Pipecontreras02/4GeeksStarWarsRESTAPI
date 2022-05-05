from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


db = SQLAlchemy()

Base = declarative_base()

association_people = Table('people_favorites', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('people_id', db.ForeignKey('people.id'), primary_key=True))


association_planets = Table('planets_favorites', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('planets_id', db.ForeignKey('planets.id'), primary_key=True))

class User(db.Model):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250),   unique=False, nullable=False)
    people = db.relationship("People", secondary=association_people)
    planets = db.relationship("Planets", secondary=association_planets)

    """ character = relationship("Character",
                    secondary=association_table)
    starship = relationship("Starship",
                    secondary=association_table)
    planet = relationship("Planet",
                    secondary=association_table) """

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
                        # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(20))
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(250))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(25))
    homeworld = db.Column(db.String(250))
    films = db.Column(db.String(250))
    species = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "films": self.films,
            "species": self.species        
                        # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    climate = db.Column(db.String(250))
    gravity = db.Column(db.Integer)
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.Integer)
    population = db.Column(db.Integer)
    residents = db.Column(db.String(250))
    films = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "residents": self.residents,
            "films": self.films        
                        # do not serialize the password, its a security breach
        }