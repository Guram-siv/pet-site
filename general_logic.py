import psycopg2
from config import config
from datetime import date as dt


from models import Pet, Convert_id, Login, Person

#from main import logged_in, person

connection = None
params = config()
connection = psycopg2.connect(**params)
curs = connection.cursor()



def init_login(mail, password):
    login = Login(mail, password)
    return login

def init_person(name, lastname, mail, password, phone, address):
    person = Person(name, lastname, mail, password, phone, address)
    return person


def register_pet(logged_in, person, login):
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
            break

        except:
            print("incorrect input, try again.")
            continue

    pet = Pet(petname, species, breed, gender, bdate)
    if logged_in == False:
        pet.register(person.person_id) #its a class here, dont get confused
    elif logged_in == True:
        pet.register(login.person_id) #same here

# log in fuctions from here


def owner_login(login, action):
    if action == "1":

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

    elif action == "2":
        owner_id = Convert_id.person_to_owner(login.person_id)
        curs.execute(
            "SELECT * FROM visits WHERE owner_id = %s;", (owner_id, ))
        result = curs.fetchone()
        if result is not None:

            visits = result[0]
            for visit in visits:
                visit_id = visit[0]
                vet_id = visit[1]
                pet_id = visit[2]
                owner_id = visit[3]
                diagnosis = visit[4]
                treatment = visit[5]
                visitdate = visit[6]
                print(f"Visit ID: {visit_id},"
                        f"Vet ID: {vet_id}, Pet ID: {pet_id}, Owner ID: {owner_id},"
                        f"Diagnosis: {diagnosis}, Treatment: {treatment}, Date: {visitdate}")
        else:
            print("you dont have any visits\n")

    elif action == "3":
        register_pet(True, None, login)

    else:
        print("the input was incorrect...")


def staff_login(login, type, action):

    if action == "1":
        curs.execute("SELECT persons.name, persons.lastname, persons.status, pets.name, pets.species, "
                        "pets.breed FROM persons JOIN pets ON persons.id=pets.owner_id "
                        "WHERE persons.status in (1, 3, 5, 7)")
        owners = curs.fetchall()
        for owner in owners:
            owner_name = owner[0] + " " + owner[1]
            status = owner[2]
            pet_name = owner[3]
            pet_type = owner[4]
            pet_breed = owner[5]
            print(
                f"Owner name: {owner_name}, Status: {status},Pet name: {pet_name}, Pet type: {pet_type}, Pet breed: {pet_breed}")

    elif action == "2":
        curs.execute(
            "SELECT name, lastname, phone,"
            "id, status FROM persons WHERE"
            " status IN (4, 5)")
        vets = curs.fetchall()
        for vet in vets:
            vet_name = vet[0] + " " + vet[1]
            vet_status = "is vet" if vet[4] == 5 else ""
            vet_phone = vet[2]
            vet_id = vet[3]
            print(
                f"Vet name: {vet_name}, "
                f"Status: {vet_status}, "
                f"Phone: {vet_phone},"
                f"ID: {vet_id}")

    elif action == "3":
        curs.execute("SELECT p.name, p.species, p.breed\
                    , o.owner_id, per.name, per.lastname \
                    FROM pets p \
                    JOIN owners o ON p.owner_id = o.owner_id \
                    JOIN persons per ON o.person_id = per.id")
        pet_owners = curs.fetchall()
        for pet_owner in pet_owners:
            pet_name = pet_owner[0]
            pet_species = pet_owner[1]
            pet_breed = pet_owner[2]
            owner_id = pet_owner[3]
            owner_name = pet_owner[4]
            owner_lastname = pet_owner[5]
            print(
                f"Pet name: {pet_name},"
                f"Species: {pet_species},"
                f"Breed: {pet_breed},"
                f"Owner name: {owner_name} {owner_lastname},"
                f"Owner ID: {owner_id}")
    if type == 3 or type == 7:

        if action == "4":
            register_pet(True, None, login)
            if type == 3:
                curs.execute(
                    "UPDATE persons SET status = 3 WHERE id = %s", (login.person_id, ))
                connection.commit()
            else:
                pass

        elif action == "5":
            owner_id = Convert_id.person_to_owner(login.person_id)
            pets = Pet.from_db(owner_id)
            for pet in pets:
                print(str(pet))
    
    else:
        print("the input was incorrect...")


def vet_login(login, type, action):

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
            print("the input was incorrect...")
