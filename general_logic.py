from datetime import date as dt

from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import joinedload

from models import (
    Person,
    Pet,
    Vet,
    HelpCentre,
    Type,
    Speciality,
    Owner,
    Visit,
    session,
)


def login(mail, password):
    try:
        person = session.query(Person).filter_by(mail=mail, password=password).one()
        if person.mail == mail:
            if person.password == password:
                return person
                
            else:
                print("password was incorrect.")
        else:
            print("mail was incorrect.")
    except NoResultFound:
        raise
        return None



def register_person():
    while True:
        try:
            print("~~~~~~~~~~~~~~~~~~~\nWelcome\n~~~~~~~~~~~~~~~~~~~")
            choice = int(input("who are you?\n" +
            "1) Pet owner\n" +
            "2) Staff member\n" +
            "3) Pet owner and Staff member\n" +
            "4) Vet\n" +
            "5) Pet owner and Vet\n" +
            "6) Staff member and Vet\n" +
            "7) Pet owner, staff member and vet\n: "))

        except ValueError:
            print("Please enter the given numbers...")
            continue
        while True:
            try:
                name = input("Name: ")
                lastname = input("Lastname: ")
                phone = int(input("Phone number: "))
                mail = input("Mail: ")
                password = input("password: ")
                address = input("Address: ")
                date = dt.today()
                person = Person(name=name, lastname=lastname, phone=phone,
                                mail=mail, address=address, created=date,
                                type=choice, password=password)
                session.add(person)
                session.commit()
                break
            except ValueError:
                session.rollback()
                print("The input was incorrect try again")
                continue
        if choice == 2 or choice == 3:
            try:
                helpcentre = HelpCentre(person_id=person.id, type=choice)
                session.add(helpcentre)
                session.commit()
            except:
                print("something went wrong in section choice 2/3...")
                session.rollback()

        elif choice == 4 or choice == 5:
            try:
                vet = Vet(person_id=person.id)
                session.add(vet)
                session.commit()
            except:
                print("something went wrong in section choice 4/5...")
                session.rollback()

        elif choice == 6 or choice == 7:
            try:
                helpcentre = HelpCentre(person_id=person.id, type=choice)
                vet = Vet(person_id=person.id)
                session.add_all([helpcentre, vet])
                session.commit()
            except:
                print("something went wrong in section choice 6/7...")
                session.rollback()

        if choice == 1 or choice == 3 or choice == 5 or choice == 7:
            try:
                owner = Owner(person_id=person.id)
                session.add(owner)
                session.commit()

            except:
                print("something went wrong in section choice 1/3/5/7...")
                session.rollback()

        return person  #returns the whole object to iterate



def register_pet(person_id):
    while True:
        try:
            petname = input("Pet name: ")
            species = input("Type: ")
            breed = input("breed: ")
            gender = input("gender(M - male / F - female): ")
            byear = int(input("pet birth year: "))
            bmonth = int(input("Month: "))
            bday = int(input("Day: "))
            bdate = dt(byear, bmonth, bday)

            print("pass 1")

            # Query the owner model to get the owner_id
            owner = session.query(Owner).filter_by(person_id = person_id).one()
            owner_id = owner.owner_id

            print("pass 2")

            # Create a new pet object and add it to the session
            pet = Pet(name=petname, species=species, 
                      breed=breed, gender=gender, 
                      birth_date=bdate, owner_id=owner_id)
            session.add(pet)
            session.commit()
            break
        except SQLAlchemyError:
            print("incorrect input, try again.")
            continue

    



def owner_login(person, action): #person here is a model from models.py
    if action == "1":
        try:
            owner = session.query(Owner).filter_by(person_id=person.id).one()
            owner_id = owner.owner_id
            pets = session.query(Pet).filter_by(owner_id=owner_id).all()
            if not pets:
                print("You don't have any pets...")
            else:
                for pet in pets:
                    print(f"Pet ID: {pet.pet_id}, Pet name: {pet.name}, "
                          f"type: {pet.species}, Breed: {pet.breed}, Recent vaccination: {pet.recent_vaccination}")
        except NoResultFound:
            session.rollback()
            raise
    elif action == "2":
        owner = session.query(Owner).filter_by(person_id=person.id).one()
        owner_id = owner.owner_id
        visits = session.query(Visit).filter_by(owner_id=owner_id).all()
        if visits:
            for visit in visits:
                visit_id = visit.visit_id
                vet_id = visit.vet_id
                pet_id = visit.pet_id
                owner_id = visit.owner_id
                diagnosis = visit.diagnosis
                treatment = visit.treatment
                visit_date = visit.date
                print(f"Visit ID: {visit_id}, Vet ID: {vet_id}, "
                      f"Pet ID: {pet_id}, Owner ID: {owner_id}, "
                      f"Diagnosis: {diagnosis}, Treatment: {treatment}, "
                      f"Date: {visit_date}")
        else:
            print("You don't have any visits.\n")
    elif action == "3":
        register_pet(person.id)
    else:
        print("The input was incorrect...")

#need to look into this function


def vet_login(person, action):
    vet = session.query(Vet).filter_by(person_id = person.id).one()
    if action == "1":
        try:
            owner_id = int(input("Please input owner id: "))
            pet_id = int(input("Please input pet id: "))
            diagnosis = input("What was the diagnosis?: ")
            vaccination = input("Was pet vaccinated? (y/n): ")
            visit_date = dt.today()
            pet = session.query(Pet).filter_by(pet_id=pet_id).first()

            if vaccination == "y":
                if pet:
                    pet.recent_vaccination = visit_date
                    session.commit()

                else:
                    print(f"There is no pet with id of {pet_id}")

            treat = input("Does pet have current treatment? (y/n):")

            if treat == "y":
                treatment = input("explain the treatment: ")
                if pet:
                    pet.current_treatment = treatment
                    session.commit()

            visit = Visit(vet_id=vet.vet_id, pet_id=pet_id, owner_id=owner_id,
                          diagnosis=diagnosis, date=visit_date)
            session.add(visit)
            session.commit()
            print("visit added successfully...\n\n")
        except Exception as error:
            session.rollback()
            print(f"visit was not added... see error: {error}")

    elif action == "2":
        vet_id = vet.vet_id
        vet_name = person.name
        vet_lastname = person.lastname
        visits = session.query(Visit).join(Owner).join(Person).filter(Visit.vet_id == vet_id).all()
        if visits:  # check if visits list is not empty
            for visit in visits:
                print(f"Visit ID: {visit.visit_id}, My name: {vet_name} {vet_lastname}, Pet ID: {visit.pet_id},"
                      f" Owner: {visit.owner.person.name} {visit.owner.person.lastname}, Diagnosis: {visit.diagnosis},"
                      f" Treatment: {visit.treatment}, Date: {visit.date}")
        else:
            print("\nyou dont have any visits\n")

    elif action == "3":
        while True:
            choose = input(
                "\n1) add my specialty\n2) list specialties\n3) My Specialities \n0) Go to main menu\n:")

            if choose == "1":
                speciality = input("My specialty: ")
                speciality = speciality.lower().capitalize()
                specialties = session.query(Speciality).filter_by(specialty=speciality).one()

                if specialties:
                    vet_id = vet.vet_id
                    spec_id = specialties.spec_id
                    vet.spec_id = spec_id
                    session.commit()
                    print("specialty added successfully...\n")

                else:
                    print(f"There is no {speciality} specialty in our database,"
                          "either contact the staff or try again")
                    continue

            elif choose == "2":
                specialties = session.query(Speciality).all()
                for s in specialties:
                    print(s.specialty)
            
            elif choose == "3":
                result = session.query(Vet).join(Speciality).filter(Vet.vet_id == vet.vet_id)
                print("\nyour specialities are:")
                for r in result:
                    print(r.speciality.specialty)
            elif choose == "0":
                print("\n")
                break

            else:
                print("The input was incorrect...")
                continue


#staff login needs fixing

def staff_login(person, action):
    if action == "1":
        owners = session.query(Owner).join(Person).all()
        for owner in owners:
            person_name = owner.person.name if owner.person else "Unknown"
            
            pets = session.query(Pet).filter_by(owner_id = owner.owner_id)
            r = 0
            for pet in pets:
                count = r + 1
            print(f"ID: {owner.owner_id}, Owner: {person_name}, Pet count: {count}")
    
    

    elif action == "2":
        vets = session.query(Vet).all()
        if vets:
            for vet in vets:
                result = session.query(Person).filter_by(id =  vet.person_id).one()
                name = result.name
                try:
                    result = session.query(Speciality).filter_by(spec_id = vet.spec_id).one()
                    if result is not None:
                        speciality = result.specialty
                    else:
                        speciality = "No Speciality registered"
                except:
                    raise
                print(f"Vet id: {vet.vet_id}, Vet name {name}, Specialises in {speciality}")
        else:
            print("No Vets in current Database...")

    elif action == "3": #does not work as it should
        pets = session.query(Pet).join(Owner).join(Person).all()
        for pet in pets:
            owner_name = pet.owner.person.name
            print(f"ID: {pet.pet_id}, Pet: {pet.name}, Owner: {owner_name}, Current_treatment: {pet.current_treatment}")
    
    elif person.type == 3 or person.type == 7:    
        if action =="4":
            register_pet(person.id)

        elif action == "5":
            try:  
                owner = session.query(Owner).filter_by(person_id=person.id).one()
                owner_id = owner.owner_id
                pets = session.query(Pet).filter_by(owner_id=owner_id).all()
                if not pets:
                    print("You don't have any pets...")
                else:
                    for pet in pets:
                        print(f"Pet ID: {pet.pet_id}, Pet name: {pet.name}, "
                            f"type: {pet.species}, Breed: {pet.breed}, Recent vaccination: {pet.recent_vaccination}")
            except NoResultFound:
                session.rollback()
                raise
    else:
        print("Invalid action!")