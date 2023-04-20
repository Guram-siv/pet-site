#models file, every table objectified, general purpose:
#to create objects of tables and use that objects in general_logic.py


from flask import Flask
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "'postgresql://name@example.com:admin@localhost:5050/testdb'"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



class Status(db.Model):
    __tablename__ = 'statuses'
    status = db.Column(db.Integer, primary_key=True, unique=True)
    explanation = db.Column(db.String(50))


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    mail = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    created = db.Column(db.DateTime)
    status = db.Column(db.Integer, db.ForeignKey('statuses.status'))
    status_rel = db.relationship(Status)
    password = db.Column(db.String(100), nullable=False)


class Owner(db.Model):
    __tablename__ = 'owners'
    owner_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person_rel = db.relationship(Person)

class Speciality(db.Model):
    __tablename__ = 'specialities'
    spec_id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(50), unique = True)
    description = db.Column(db.String(150))


class Vet(db.Model):
    __tablename__ = 'vets'
    vet_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person_rel = db.relationship(Person)


class SpecCombo(db.Model):
    __tablename__ = 'spec_combo'
    id = db.Column(db.Integer, primary_key=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.vet_id'))
    vet_rel = db.relationship(Vet)
    spec_id = db.Column(db.Integer, db.ForeignKey('specialities.spec_id'))
    spec_rel = db.relationship(Speciality)


class Pet(db.Model):
    __tablename__ = 'pets'
    pet_id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(50))
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(2))
    medical_condition = db.Column(db.String(50))
    current_treatment = db.Column(db.String(50))
    resent_vaccination = db.Column(db.Date)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'))
    owner_rel = db.relationship(Owner)


class HelpCentre(db.Model):
    __tablename__ = 'help_centre'
    staff_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person_rel = db.relationship(Person)
    status = db.Column(db.Integer)


class Visit(db.Model):
    __tablename__ = 'visits'
    visit_id = db.Column(db.Integer, primary_key=True)
    vet_id = db.Column(db.Integer, db.ForeignKey('vets.vet_id'))
    vet_rel = db.relationship(Vet)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'))
    pet_rel = db.relationship(Pet)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'))
    owner_rel = db.relationship(Owner)
    diagnosis = db.Column(db.String(100))
    treatment = db.Column(db.String(50))
    date = db.Column(db.Date)
