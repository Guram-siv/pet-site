from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import relationship


engine = create_engine('postgresql://postgres:postgres@localhost:5432/petv2')
# engine = create_engine('sqlite:///:test.db', echo=True)
Base = declarative_base()

class Type(Base):
    __tablename__ = 'types'
    type = Column(Integer, primary_key=True, unique=True)
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
    type = Column(Integer, ForeignKey('types.type'))
    person_type = relationship(Type)
    password = Column(String(100), nullable=False)


class Owner(Base):
    __tablename__ = 'owners'
    owner_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship(Person)


class Speciality(Base):
    __tablename__ = 'specialities'
    spec_id = Column(Integer, primary_key=True)
    specialty = Column(String(50), unique=True)
    description = Column(String(150))


class Vet(Base):
    __tablename__ = 'vets'
    vet_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship(Person)
    spec_id = Column(Integer, ForeignKey('specialities.spec_id'))
    speciality = relationship(Speciality)

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
    owner = relationship(Owner)


class HelpCentre(Base):
    __tablename__ = 'help_centre'
    staff_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship(Person)
    type = Column(Integer, ForeignKey('types.type'))


class Visit(Base):
    __tablename__ = 'visits'
    visit_id = Column(Integer, primary_key=True)
    vet_id = Column(Integer, ForeignKey('vets.vet_id'))
    vet = relationship(Vet)
    pet_id = Column(Integer, ForeignKey('pets.pet_id'))
    pet = relationship(Pet)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'))
    owner = relationship(Owner)
    diagnosis = Column(String(100))
    treatment = Column(String(50))
    date = Column(Date)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
