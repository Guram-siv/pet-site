from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import relationship

Base = declarative_base()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/testdb')

Base.metadata.create_all(engine)

Session = sessionmaker()
session = Session()
class Status(Base):
    __tablename__ = 'statuses'
    status = Column(Integer, primary_key=True, unique=True)
    explanation = Column(String(50))


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=False)
    mail = Column(String(100), unique=True)
    address = Column(String(100))
    created = Column(DateTime)
    status = Column(Integer, ForeignKey('statuses.status'))
    status_rel = relationship(Status)
    password = Column(String(100), nullable=False)


class Owner(Base):
    __tablename__ = 'owners'
    owner_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person_rel = relationship(Person)


class Speciality(Base):
    __tablename__ = 'specialities'
    spec_id = Column(Integer, primary_key=True)
    specialty = Column(String(50), unique=True)
    description = Column(String(150))


class Vet(Base):
    __tablename__ = 'vets'
    vet_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person_rel = relationship(Person)


class SpecCombo(Base):
    __tablename__ = 'spec_combo'
    id = Column(Integer, primary_key=True)
    vet_id = Column(Integer, ForeignKey('vets.vet_id'))
    vet_rel = relationship(Vet)
    spec_id = Column(Integer, ForeignKey('specialities.spec_id'))
    spec_rel = relationship(Speciality)


class Pet(Base):
    __tablename__ = 'pets'
    pet_id = Column(Integer, primary_key=True)
    species = Column(String(50))
    breed = Column(String(100))
    gender = Column(String(2))
    medical_condition = Column(String(50))
    current_treatment = Column(String(50))
    recent_vaccination = Column(Date)
    name = Column(String(50))
    birth_date = Column(Date)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'))
    owner_rel = relationship(Owner)


class HelpCentre(Base):
    __tablename__ = 'help_centre'
    staff_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person_rel = relationship(Person)
    status = Column(Integer)


class Visit(Base):
    __tablename__ = 'visits'
    visit_id = Column(Integer, primary_key=True)
    vet_id = Column(Integer, ForeignKey('vets.vet_id'))
    vet_rel = relationship(Vet)
    pet_id = Column(Integer, ForeignKey('pets.pet_id'))
    pet_rel = relationship(Pet)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'))
    owner_rel = relationship(Owner)
    diagnosis = Column(String(100))
    treatment = Column(String(50))
    date = Column(Date)




