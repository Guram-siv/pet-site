import psycopg2
from config import config
from datetime import date, datetime

connection = None
params = config()
connection = psycopg2.connect(**params)
curs = connection.cursor()


class Person:

    def __init__(self, name, lastname, mail, password,
                 person_id=None, phone=None, address=None, user_type=None) -> None:
        self.person_id = person_id
        self.name = name
        self.lastname = lastname
        self.mail = mail
        self.password = password
        self.phone = phone
        self.address = address

    def input_data(self, user_type):
        self.name = input("Name: ")
        self.lastname = input("Lastname: ")
        self.phone = int(input("Phone number: "))
        self.mail = input("Mail: ")
        self.password = input("password: ")
        self.address = input("Address: ")
    def register(self, user_type):
        try:
            self.status = user_type
            created = date.today()
            curs.execute('''INSERT INTO persons(name, lastname, mail, password, phone, address, created, status) 
      VALUES (%s, %s, %s, %s, %s, %s, %s,%s )''', (
                self.name, self.lastname, self.mail, self.password, self.phone, self.address, created, self.status))
            connection.commit()
            print("registration completed succesfully")
            curs.execute(f"SELECT id FROM persons WHERE mail = '{self.mail}' AND password = '{self.password}'")
            result = curs.fetchone()
            self.person_id = result[0]

        except (Exception, psycopg2.DatabaseError) as error:
            raise
            #print(error)

    @classmethod
    def _tuple_to_person(cls, person_tuple):
        person = cls(
            person_id=person_tuple[0],
            name=person_tuple[1],
            lastname=person_tuple[2],
            mail=person_tuple[3],
            password=person_tuple[4],
            address=person_tuple[5],
            phone=person_tuple[6],
            user_type=person_tuple[7]
        )
        return person

    @classmethod
    def get_all(cls):
        try:
            curs.execute(
                "SELECT id, name, lastname, mail, password, address, phone, status FROM persons")
            persons_collection = curs.fetchall()
            persons = []
            for person_tuple in persons_collection:
                person = cls._tuple_to_person(person_tuple)
                persons.append(person)
            return persons
        except psycopg2.DatabaseError as db_error:
            print(f"Can't get user data, Error: {db_error}")

    @classmethod
    def person_from_db(cls, user_id):
        try:
            curs.execute(
                f"SELECT id, name, lastname, mail, password, address, phone, status FROM persons WHERE id = {user_id}")
            person_tuple = curs.fetchone()
            print(person_tuple)
            person = cls._tuple_to_person(person_tuple)
            return person
        except psycopg2.DatabaseError as db_error:
            print(f"Can't get user data, Error: {db_error}")

    def __str__(self):
        return f"User (Name: {self.name}, {self.lastname})"

    def __repr__(self):
        return f"User (Name: {self.name}, {self.lastname})"

class Pet:
    def __init__(self, petname, species, breed, gender, byear, bmonth, bday) -> None:
        self.petname = petname
        self.species = species
        self.breed = breed
        self.gender = gender
        self.byear = byear
        self.bmonth = bmonth
        self.bday = bday


    def input_data(self):
        self.petname = input("Pet name: ")
        self.species = input("Type: ")
        self.breed = input("breed: ")
        self.gender = input("gender(M - male / F - female): ")
        self.byear = int(input("pet birth year: "))
        self.bmonth = int(input("Month: "))
        self.bday = int(input("Day: "))
        self.birthdate = date(self.byear, self.bmonth, self.bday)
        

    def register(self, person_id):
        try:
            self.person_id = person_id
            curs.execute(
                "INSERT INTO owners(person_id) VALUES (%s)", (self.person_id, ))
            self.owner_id = Convert_id.person_to_owner(self.person_id)
            curs.execute('''INSERT INTO pets(species, breed, sex, name, birth_date, owner_id) 
        VALUES (%s, %s, %s, %s, %s, %s)''', (self.species, self.breed, self.gender, self.petname, self.birthdate, self.owner_id))
            self.pet_id = Convert_id.owner_to_pet(self.owner_id)
            connection.commit()     
            print(f"Pet registered succesfully! your pet was granted id: {self.pet_id}")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    @classmethod
    def _tuple_to_pet(cls, pet_tuple):
        pet = cls(
            pet_id = pet_tuple[0],
            species = pet_tuple[1],
            breed = pet_tuple[2],
            gender = pet_tuple[3],
            medical_condition = pet_tuple[4],
            current_treatment = pet_tuple[5],
            resent_vaccination = pet_tuple[6],
            name = pet_tuple[7],
            birth_date = pet_tuple[8],
            owner_id = pet_tuple[9]
        )
        return pet


    @classmethod
    def get_all(cls):
        try:
            curs.execute(
                "SELECT * FROM pets")
            pets_collection = curs.fetchall()
            pets = []
            for pet_tuple in pets_collection:
                pet = cls._tuple_to_pet(pet_tuple)
                pets.append(pet)
            return pets
        except psycopg2.DatabaseError as db_error:
            print(f"Can't get user data, Error: {db_error}")
    

    @classmethod
    def from_db(cls, owner_id):
        try:
            curs.execute(
                f"SELECT * FROM pets WHERE owner_id = {owner_id}")
            pet_tuple = curs.fetchone()
            print(pet_tuple)
            pet = cls._tuple_to_pet(pet_tuple)
            return pet
        except psycopg2.DatabaseError as db_error:
            print(f"Can't get user data, Error: {db_error}")


class Login:
    def __init__(self, mail, userpassword, person_type=None, log = "No"):
        self.mail = mail
        self.userpassword = userpassword
        self.person_type = person_type
        self.log = log

        #ar damaviwydes mail gavxado unique 
        #radgan mere userebi aireva
    def login(self):
        self.mail = input("Please enter your email: ")
        curs.execute("SELECT password FROM persons WHERE mail = %s", (self.mail, ))
        self.userpassword = curs.fetchone()
        if self.userpassword is not None:
            password = input("Please enter your password: ")
            if self.userpassword[0] == password:
                curs.execute(
                    "SELECT id FROM persons WHERE mail = %s AND password = %s", (self.mail, password))
                person = curs.fetchone()
                self.person_id = person[0]
                self.log = "Yes"
            else:
                print("Incorrect password.")
        else:
            print("Email not found.")
        self.person_type = Convert_id.person_to_type(self.person_id)


    def owner(self):
        while True:
                action = input(
                    "\n\n\nWhat should we do?\n1) my pets\n2) my visits\n0) log out \nq) Exit program \n: ")
                if action == "1":
                    owner_id = Convert_id.person_to_owner(self.person_id)
                    pet = Pet.from_db(owner_id)
                    species = pet[1]
                    breed = pet[2]
                    gender = pet[3]
                    medical_condition = pet[4]
                    current_treatment = pet[5]
                    resent_vaccination = pet[6]
                    pet_name = pet[7]
                    birth_date = pet[8]
                    print(f"Species: {species}, Breed: {breed}, Gender: {gender}, Medical Condition: {medical_condition}, Current Treatment: {current_treatment}, Resent Vaccination: {resent_vaccination}, Name: {pet_name}, Birth Date: {birth_date}")
                elif action == "2":
                    curs.execute("SELECT * FROM visits WHERE person_id = %s;", (self.person_id, ))
                    result = curs.fetchone()
                    visits = result[0]
                    for visit in visits:
                        visit_id = visit[0]
                        vet_id = visit[1]
                        pet_id = visit[2]
                        owner_id = visit[3]
                        diagnosis = visit[4]
                        treatment = visit[5]
                        visitdate = visit[6]
                    if visits is None:
                        print("you dont have pets, hence you got no visits")
                    else:
                        print(f"Visit ID: {visit_id}, Vet ID: {vet_id}, Pet ID: {pet_id}, Owner ID: {owner_id}, Diagnosis: {diagnosis}, Treatment: {treatment}, Date: {visitdate}")
                elif action == "0":
                    exit = False
                    break
                elif action == "q":
                    exit = True
                    break
                else:
                    print("the input was incorrect...")
                    continue
        return exit # returns exit so after the loops decides what to do


    def staff(self):
        while True:
            print()
            action = input("what action should we do?\n1) List every owner\n2) List every vet\
    \n3) List every pet\n4) Add my pet(makes me owner\staff memeber)\n5) List my pets(only for pet owners)\
    \n0) log out\nq) quit the program \n: ")
            print()
            if action == "1":
                curs.execute("SELECT persons.name, persons.lastname, persons.status, pets.name, pets.type, pets.breed FROM persons JOIN pets ON persons.id = pets.owner_id WHERE persons.status in (1, 3, 5, 7)")
                owners = curs.fetchall()
                for owner in owners:
                    owner_name = owner[0] + " " + owner[1]
                    status = owner[2]
                    pet_name = owner[3]
                    pet_type = owner[4]
                    pet_breed = owner[5]
                print(f"Owner name: {owner_name}, Status: {status}, Pet name: {pet_name}, Pet type: {pet_type}, Pet breed: {pet_breed}")

            elif action == "2":
                curs.execute(
                    "SELECT name, lastname, phone, id, status FROM persons WHERE status IN (4, 5)")
                vets = curs.fetchall()
                for vet in vets:
                    vet_name = vet[0] + " " + vet[1]
                    vet_status = "is vet" if vet[4] == 5 else ""
                    vet_phone = vet[2]
                    vet_id = vet[3]
                print(f"Vet name: {vet_name}, Status: {vet_status}, Phone: {vet_phone}, ID: {vet_id}")

            elif action == "3":
                curs.execute("SELECT pets.name, pets.species, pets.breed, persons.name, pets.pet_id || ' ' || persons.lastname as owner_name FROM pets JOIN persons ON pets.owner_id = persons.id")
                pet_owners = curs.fetchall()
                for pet_owner in pet_owners:
                    pet_name = pet_owner[0]
                    pet_species = pet_owner[1]
                    pet_breed = pet_owner[2]
                    owner_name = pet_owner[3]
                    owner_id = pet_owner[4]
                print(f"Pet name: {pet_name}, Species: {pet_species}, Breed: {pet_breed}, Owner name: {owner_name}, Owner ID: {owner_id}")

            elif action == "4":
                Pet.register(self.person_id)
                type = Convert_id.person_to_type(self.person_id)
                if type == "4":
                    curs.execute(
                        "UPDATE persons SET status = 5 WHERE id = %s", (self.person_id, ))
                    connection.commit()
                else:
                    pass
            elif action == "5":
                owner_id = Convert_id.person_to_owner(self.person_id)
                if owner_id is not None:
                    pet = Pet.from_db(owner_id)
                    species = pet[1]
                    breed = pet[2]
                    gender = pet[3]
                    medical_condition = pet[4]
                    current_treatment = pet[5]
                    resent_vaccination = pet[6]
                    pet_name = pet[7]
                    birth_date = pet[8]
                    print(f"Species: {species}, Breed: {breed}, Gender: {gender}, Medical Condition: {medical_condition}, Current Treatment: {current_treatment}, Resent Vaccination: {resent_vaccination}, Name: {pet_name}, Birth Date: {birth_date}")
                else:
                    print("it appears you dont have a pet, add it from main menu.")
            elif action == "0":
                exit = False
                break
            elif action == "q":
                exit = True
                break
            else:
                print("the input was incorrect...")
                continue
        return exit

    def vet(self):
        while True:
            action = input("What action should we perform?\n1) add a new entry in visits\n2) List my med history\
    \n3) add my speciality \n4) add my pet(makes me owner/vet)\n0) log out\nq) exit program")
            if action == "1":
                owners_id = input("Please input owner id: ")
                pets_id = input("Please input pet id: ")
                diagnosis = input("What was the diagnosis?: ")
                vaccination = input("Was pet vaccinated? (y/n): ")
                visitdate = date.today()
                if vaccination == "y":
                    vacdate = date.today()
                    curs.execute(
                        "INSERT INTO pets(resent_vaccination) VALUES (%s) WHERE pet_id = %s", (vacdate, pets_id))
                    connection.commit()
                else:
                    pass
                treat = input("Does pet have current treatment? (y/n):")
                if treat == "y":
                    treatment = input("explain the treatment: ")
                    curs.execute(
                        "INSERT INTO pets(current_treatment) VALUES (%s) WHERE pet_id = %s", (treatment, pets_id))
                    connection.commit()
                else:
                    pass
                curs.execute("INSERT INTO visits(vet_id, pet_id, owner_id, diagnosis, date) VALUES (%s, %s, %s, %s, %s)",
                            (vet_id, pets_id, owners_id, diagnosis, visitdate))
                connection.commit()
            elif action == "2":
                curs.execute("SELECT * FROM visits WHERE vet_id = %s", (vet_id, ))
                visits = curs.fetchall()
                for visit in visits:
                    visit_id = visit[0]
                    vet_id = visit[1]
                    pet_id = visit[2]
                    owner_id = visit[3]
                    diagnosis = visit[4]
                    treatment = visit[5]
                    date = visit[6]
                print(f"Visit ID: {visit_id}, Vet ID: {vet_id}, Pet ID: {pet_id}, Owner ID: {owner_id}, Diagnosis: {diagnosis}, Treatment: {treatment}, Date: {date}")

            elif action == "3":
                while True:
                    choose = input(
                        "1) add my speciality\n2) list specialities\n0) Go to main menu")
                    if choose == "1":
                        speciality = "My speciality: "
                        speciality.lower()
                        speciality.capitalize()
                        curs.execute("SELECT specialty FROM specialities")
                        results = curs.fetchall()
                        specialities_list = [result[0] for result in results]
                        if speciality in specialities_list:
                            curs.execute(
                                "SELECT spec_id FROM specialities WHERE specialty = %s", (speciality))
                            result = curs.fetchone()
                            spec_id = result[0]
                            curs.execute(
                                "INSERT INTO spec_combo(vet_id, spec_id) VALUES (%s, %s)", (vet_id, spec_id))
                            connection.commit()
                        else:
                            print(
                                f"There is no {speciality} speciality in our database, either contact the staff or try again")
                            continue
                    elif choose == "2":
                        curs.execute("SELECT specialty FROM specialities")
                        results = curs.fetchall()
                        specialities_list = [result[0] for result in results]
                        for s in specialities_list:
                            print(s)
                    elif choose == "3":
                        break

            elif action == "4":
                Pet.register(self.person_id)
                stat = Convert_id.person_to_type(self.person_id)
                if stat == "4":
                    curs.execute(
                        "UPDATE persons SET status = 5 WHERE id = %s", (self.person_id))
                    connection.commit()
                else:
                    pass
            elif action == "0":
                exit = False
                break
            elif action == "q":
                exit = True
                break
            else:
                print("the input was incorrect...")
                continue
        return exit



class Convert_id:
    def person_to_owner(person_id):
        curs.execute(f"SELECT owner_id FROM owners WHERE person_id = {person_id}")
        result = curs.fetchone()
        owner_id = result[0]
        return owner_id
    
    def owner_to_pet(owner_id):
        curs.execute(f"SELECT pet_id FROM pets WHERE owner_id = {owner_id}")
        result = curs.fetchone()
        pet_id = result[0]
        return pet_id
    
    def person_to_vet(person_id):
        curs.execute(f"SELECT vet_id FROM vets WHERE person_id = {person_id}")
        result = curs.fetchone()
        vet_id = result[0]
        return vet_id
    
    def owner_to_visit(owner_id):
        curs.execute(f"SELECT visit_id FROM visits WHERE owner_id = {owner_id} ")
        result = curs.fetchone()
        visit_id = result[0]
        return visit_id
    
    def person_to_type(person_id):
        curs.execute(f"SELECT status FROM persons WHERE id = {person_id}")
        result = curs.fetchone()
        vet_id = result[0]
        return vet_id
    


while True:
    action = input("login or register\n: ")
    if action == "login":
        action = input("login or register\n: ")
    if action == "login":
        login = Login("", "")
        login.login()
        if log == "No":
            print("Login was unsuccesfull, try again...")
            continue
        elif log == "Yes":
            print("Login was succesfull...")
            pass
        if login.person_type == 1:
            exit = login.owner()
            if exit == True:
                break
            else:
                continue
        elif login.person_type == 2 or login.person_type == 3:
            if login.person_type == 3:
                choise = input(
                    "It appears you have a pet... do you want to add it now?(y/n)\n:")
                if choise == "y":
                    Pet.register(login.person_id)
                elif choise == "n":
                    pass
                else:
                    print("something went wrong with input! logging out")
                    continue
            else:
                exit = login.staff()
                if exit == True:
                    break
                else:
                    continue

        elif login.person_type == 4 or login.person_type == 5:
            if login.person_type == 5:
                choise = input(
                    "It appears you have a pet... do you want to add it now?(y/n)\n:")
                if choise == "y":
                    Pet.input_data()
                    Pet.register(login.person_id)
                elif choise == "n":
                    pass
                else:
                    print("something went wrong with input! logging out")
                    continue
            vet_id = Convert_id.person_to_vet(login.person_id)
            print(f"Hello Dear vet, your id is {vet_id}")
            exit = login.vet()
            if exit == True:
                break
            else:
                continue
        elif login.person_type == 6 or login.person_type == 7:
            print("Hello Dear staff/vet")
            if login.person_type == 7:
                choise = input(
                    "It appears you have a pet... do you want to add it now?(y/n)\n:")
                if choise == "y":
                    Pet.input_data()
                    Pet.register(login.person_id)
                elif choise == "n":
                    pass
            while True:
                choose = input(
                    "do you want to enter as staff or vet?\n1)Staff member\n2)Vet\n: ")
                if choose == "1":
                    print("You are in staff sub menu")
                    login.staff()
                if choose == "2":
                    print("You are in vet sub menu")
                    login.vet()

    elif action == "register":
        try:
            print("~~~~~~~~~~~~~~~~~~~\nWelcome\n~~~~~~~~~~~~~~~~~~~")
            choise = int(input("\
who are you?\n\
1) Pet owner\n\
2) Staff member\n\
3) Pet owner and Staff member\n\
4) Vet\n\
5) Pet owner and Vet\n\
6) Staff member and Vet\n\
7) Pet owner, staff member and vet\n: "))
        except:
            print("Please enter the given numbers...")

        person = Person("", "", "", "")
        person.input_data(choise)
        person.register()

        if choise == 2 or choise == 3:
            curs.execute(
                "INSERT INTO help_centre(person_id, status) VALUES (%s, %s)", (person.person_id, choise))

        elif choise == 4 or choise == 5:
            curs.execute(
                "INSERT INTO vets(person_id) VALUES(%s)", (person.person_id,))

        elif choise == 6 or choise == 7:
            curs.execute(
                "INSERT INTO help_centre(person_id, status) VALUES (%s, %s)", (person.person_id, choise))
            curs.execute(
                "INSERT INTO vets(person_id) VALUES(%s)", (person.person_id,))

        if choise == 1 or choise == 3 or choise == 5 or choise == 7:
            haspet = input(
                "Do you want to register a pet?\n(y - yes / n - no): ")
            if haspet.lower() == "y" or haspet.lower() == "yes":
                Pet.input_data()
                Pet.register(person.person_id)
            elif haspet.lower() == "n" or haspet.lower() == "no":
                log = input(
                    "do you want to return to main menu? (y - yes / n - exit): ")
                if log == "n":
                    break
                else:
                    continue
            else:
                continue
            # last = input("registration has been succesfull!")
        else:
            continue
curs.close()
connection.close()
