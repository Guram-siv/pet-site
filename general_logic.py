from datetime import date as dt

from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from models import (
    Person,
    Pet,
    Vet,
    HelpCentre,
    Status,
    Speciality,
    Owner,
    SpecCombo,
    Visit,
    session,
)


def login(mail, password):
    try:
        person = session.query(Person).filter_by(mail=mail, password=password).one()
        if person.mail == mail:
            if person.password == password:
                print("\nSuccessfully logged in...\n")
                log = "Yes"
                return person
            else:
                print("password was incorrect.")
        else:
            print("mail was incorrect.")
    except NoResultFound:
        print("Something went wrong with login")
        log = "No"


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
                                status=choice, password=password)
                session.add(person)
                session.commit()
                break
            except ValueError:
                session.rollback()
                print("The input was incorrect try again")
                continue
        if choice == 2 or choice == 3:
            try:
                helpcentre = HelpCentre(person_id=person.id, status=choice)
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
                helpcentre = HelpCentre(person_id=person.id, status=choice)
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

            # Query the owner model to get the owner_id
            owner = session.query(Owner).filter_by(person_id=person_id).one()
            owner_id = owner.id

            # Create a new pet object and add it to the session
            pet = Pet(name=petname, species=species, 
                      breed=breed, gender=gender, 
                      birth_date=bdate, owner_id=owner_id)
            session.add(pet)
            session.commit()
            break
        except SQLAlchemyError:
            session.rollback()
            print("incorrect input, try again.")
            continue

    
    


# needs fixing from here


def owner_login(person_id, action):
    if action == "1":
        try:
            owner = session.query(Owner).filter_by(person_id=person_id).one()
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
        owner = session.query(Owner).filter_by(person_id=person_id).one()
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
        register_pet(person_id)
    else:
        print("The input was incorrect...")

#need to look into this function

def vet_login(login, type, action):
    if action == "1":
        try:
            owner_id = input("Please input owner id: ")
            pet_id = input("Please input pet id: ")
            diagnosis = input("What was the diagnosis?: ")
            vaccination = input("Was pet vaccinated? (y/n): ")
            visit_date = dt.today()

            if vaccination == "y":
                pet = session.query(Pet).filter_by(pet_id=pet_id).first()
                if pet:
                    pet.recent_vaccination = visit_date
                    session.commit()

            treat = input("Does pet have current treatment? (y/n):")

            if treat == "y":
                treatment = input("explain the treatment: ")
                pet = session.query(Pet).filter_by(pet_id=pet_id).first()
                if pet:
                    pet.current_treatment = treatment
                    session.commit()

            vet_id = person_to_vet(login.person_id)
            visit = Visit(vet_id=vet_id, pet_id=pet_id, owner_id=owner_id,
                          diagnosis=diagnosis, date=visit_date)
            session.add(visit)
            session.commit()
            print("visit added successfully...\n\n")
        except Exception as error:
            session.rollback()
            print(f"visit was not added... see error: {error}")

    elif action == "2":
        vet_id = person_to_vet(login.person_id)
        visits = session.query(Visit).filter_by(vet_id=vet_id).all()
        if visits:  # check if visits list is not empty
            for visit in visits:
                print(f"Visit ID: {visit.visit_id}, Vet ID: {visit.vet_id}, Pet ID: {visit.pet_id},"
                      f" Owner ID: {visit.owner_id}, Diagnosis: {visit.diagnosis},"
                      f" Treatment: {visit.treatment}, Date: {visit.date}")
        else:
            print("\nyou dont have any visits\n")

    elif action == "3":
        while True:
            choose = input(
                "\n1) add my specialty\n2) list specialties\n0) Go to main menu\n:")

            if choose == "1":
                speciality = input("My specialty: ")
                speciality = speciality.lower().capitalize()
                specialties = session.query(SpecCombo).join(Speciality).filter_by(specialty=speciality).all()

                if specialties:
                    vet_id = person_to_vet(login.person_id)
                    spec_id = specialties[0].spec_id
                    spec_combo = SpecCombo(vet_id=vet_id, spec_id=spec_id)
                    session.add(spec_combo)
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

            elif choose == "0":
                print("\n")


#staff login is gone....

def staff_login():
    pass

'''def vet_login(login, type, action):

        if action == "1":
            try:
                owner_id = input("Please input owner id: ")
                pet_id = input("Please input pet id: ")
                diagnosis = input("What was the diagnosis?: ")
                vaccination = input("Was pet vaccinated? (y/n): ")
                visitdate = dt.today()

                if vaccination == "y":
                    vacdate = dt.today()
                    curs.execute(
                        "UPDATE pets SET resent_vaccination = %s WHERE pet_id = %s", (vacdate, pet_id))
                    connection.commit()

                else:
                    pass
                treat = input("Does pet have current treatment? (y/n):")

                if treat == "y":
                    treatment = input("explain the treatment: ")
                    curs.execute(
                        "UPDATE pets SET current_treatment = %s WHERE pet_id = %s", (treatment, pet_id))
                    connection.commit()

                else:
                    pass
                vet_id = Convert_id.person_to_vet(login.person_id)
                curs.execute(
                    "INSERT INTO visits(vet_id, pet_id, owner_id, diagnosis, date) VALUES (%s, %s, %s, %s, %s)",
                            (vet_id, pet_id, owner_id, diagnosis, visitdate))
                connection.commit()
                print("visit added succesfully...\n\n")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"visit was not added... see error: {error}")
                
        elif action == "2":

            vet_id = Convert_id.person_to_vet(login.person_id)
            curs.execute("SELECT * FROM visits WHERE vet_id = %s", (vet_id, ))
            visits = curs.fetchall()
            if visits is not None:  # check if visits list is not empty
                for visit in visits:
                    visit_id = visit[0]
                    vet_id = visit[1]
                    pet_id = visit[2]
                    owner_id = visit[3]
                    diagnosis = visit[4]
                    treatment = visit[5]
                    date = visit[6]
                    print(
                        f"Visit ID: {visit_id}, Vet ID: {vet_id}, Pet ID: {pet_id}, Owner ID: {owner_id},"
                        f" Diagnosis: {diagnosis}, Treatment: {treatment}, Date: {date}")
            else:
                print("\nyou dont have any visits\n")

        elif action == "3":
            while True:
                choose = input(
                    "\n1) add my speciality\n2) list specialities\n0) Go to main menu\n:")

                if choose == "1":
                    speciality = input("My speciality: ")
                    speciality = speciality.lower().capitalize()
                    curs.execute("SELECT specialty FROM specialities")
                    results = curs.fetchall()
                    specialities_list = [result[0] for result in results]

                    if speciality in specialities_list:
                        vet_id = Convert_id.person_to_vet(login.person_id)
                        curs.execute(
                            "SELECT spec_id FROM specialities WHERE specialty = %s", (speciality, ))
                        result = curs.fetchone()
                        spec_id = result[0]
                        curs.execute(
                            "INSERT INTO spec_combo(vet_id, spec_id) VALUES (%s, %s)", (vet_id, spec_id))
                        connection.commit()
                        print("speciality added succesfully... \n")

                    else:
                        print(
                            f"There is no {speciality} speciality in our database,"
                             "either contact the staff or try again")
                        continue

                elif choose == "2":
                    curs.execute("SELECT specialty FROM specialities")
                    results = curs.fetchall()
                    specialities_list = [result[0] for result in results]
                    for s in specialities_list:
                        print(s)

                elif choose == "0":
                    print("\n")
                    break
        if type == 5 or type == 7:
            if action == "4":
                register_pet(True, None, login)
            elif action == "5":
                try:

                    connection.rollback()
                    curs.execute("BEGIN;")

                    owner_id = Convert_id.person_to_owner(login.person_id)
                    pets = Pet.from_db(owner_id)
                    connection.commit()
                    if pets is None:
                        print("You dont have pets...")
                    else:
                        for pet in pets:
                            print(str(pet))
            
                except:
                    connection.rollback()
                    raise

        else:
            print("the input was incorrect...")'''
