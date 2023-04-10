import psycopg2
from config import config
from datetime import date as dt

connection = None
params = config()
connection = psycopg2.connect(**params)
curs = connection.cursor()



class Person:

    def __init__(self, name, lastname, mail, password, phone, address, person_id=None, user_type=None) -> None:
        self.person_id = person_id
        self.name = name
        self.lastname = lastname
        self.mail = mail
        self.password = password
        self.phone = phone
        self.address = address

    def register(self, user_type):
        try:
            
            self.status = user_type
            created = dt.today()
            curs.execute('''INSERT INTO persons(name, lastname, mail, password, phone, address, created, status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s )''', (
                self.name, self.lastname, self.mail, self.password, self.phone, self.address, created, self.status))
            connection.commit()
            print("registration completed succesfully")
            curs.execute(
                f"SELECT id FROM persons WHERE mail = '{self.mail}' AND password = '{self.password}'")
            result = curs.fetchone()
            self.person_id = result[0]

        except (Exception, psycopg2.DatabaseError) as error:
            raise
            # print(error)

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

    def __init__(self, name, species, breed, gender, birth_date,
                 pet_id=None, medical_condition=None,
                 current_treatment=None, resent_vaccination=None,
                 owner_id=None):
        self.pet_id = pet_id
        self.species = species
        self.breed = breed
        self.gender = gender
        self.medical_condition = medical_condition
        self.current_treatment = current_treatment
        self.resent_vaccination = resent_vaccination
        self.name = name
        self.birth_date = birth_date
        self.owner_id = owner_id

    def register(self, person_id):
        try:
            self.person_id = person_id
            self.owner_id = Convert_id.person_to_owner(person_id)

            if self.owner_id is None:
                curs.execute(
                    "INSERT INTO owners(person_id) VALUES (%s)", (self.person_id, ))
                curs.execute("SELECT LASTVAL()")
                self.owner_id = curs.fetchone()[0]
                connection.commit()
            else:
                pass

            curs.execute('''SELECT * FROM pets WHERE name = %s AND birth_date = %s AND owner_id = %s''',
                         (self.name, self.birth_date, self.owner_id))
            pet_exists = curs.fetchone()

            if pet_exists is None:
                curs.execute('''INSERT INTO pets(species, breed, gender, name, birth_date, owner_id)
                    VALUES (%s, %s, %s, %s, %s, %s)''',
                             (self.species, self.breed, self.gender, self.name, self.birth_date, self.owner_id))
                curs.execute("SELECT LASTVAL()")
                self.pet_id = curs.fetchone()[0]
                connection.commit()
                print(
                    f"Pet registered succesfully! your pet was granted id: {self.pet_id}")
            else:
                print("This pet already exists.")

        except psycopg2.DatabaseError as db_error:
            print(f"Error: {db_error}")

    # i need to edit this part of code, so it fits perfectly
    # it does not work as it should, it needs to append to tuple
    # and then get from tuple data that i need

    @classmethod
    def _tuple_to_pet(cls, pet_tuple):
        try:
            pet = cls(
                pet_id=pet_tuple[0],
                species=pet_tuple[1],
                breed=pet_tuple[2],
                gender=pet_tuple[3],
                medical_condition=pet_tuple[4],
                current_treatment=pet_tuple[5],
                resent_vaccination=pet_tuple[6],
                name=pet_tuple[7],
                birth_date=pet_tuple[8],
                owner_id=pet_tuple[9]
            )
            return pet
        except psycopg2.DatabaseError as db_error:
            print(f"You don't have pets, hence: {db_error}")

    @classmethod
    def get_all(cls):
        try:
            curs.execute(
                "SELECT * FROM pets")
            pets_collection = curs.fetchall()
            if pets_collection is None:
                pets = None
                return pets
            else:
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
            curs.execute(f"SELECT * FROM pets WHERE owner_id = '{owner_id}'")
            pets_collection = curs.fetchall()
            if pets_collection is None:
                pets = None
                return pets
            else:
                pets = []
                for pet_tuple in pets_collection:
                    pet = list(pet_tuple)
                    pets.append(pet)
                pets = [cls._tuple_to_pet(pet) for pet in pets]
                return pets
        except psycopg2.DatabaseError as db_error:
            print(f"Can't get user data, Error: {db_error}")

    def __str__(self):
        return f"Species: {self.species}, Breed: {self.breed}," +\
            f" Gender: {self.gender}, Medical Condition: {self.medical_condition}," +\
            f" Current Treatment: {self.current_treatment}, Resent Vaccination: " +\
            f"{self.resent_vaccination}, Name: {self.name}, Birth Date: " +\
            f"{self.birth_date}"


class Login:

    def __init__(self, mail, password, person_type=None, log="No"):
        self.mail = mail
        self.password = password
        self.person_type = person_type
        self.log = log
        

    def login(self):
        curs.execute(
            "SELECT password FROM persons WHERE mail = %s", (self.mail, ))
        self.userpassword = curs.fetchone()
        if self.userpassword is not None:
            if self.userpassword[0] == self.password:
                curs.execute(
                    "SELECT id FROM persons WHERE mail = %s AND password = %s", (self.mail, self.password))
                person = curs.fetchone()
                self.person_id = person[0]
                self.log = "Yes"
            else:
                print("Incorrect password.")

        else:
            print("Email not found.")
        self.person_type = Convert_id.person_to_type(self.person_id)

    def vet(self):
        pass

        return exit


class Convert_id:

    def person_to_owner(person_id):
        curs.execute(f"SELECT owner_id FROM owners WHERE person_id = {person_id}")
        result = curs.fetchone()
        if result is None:
            return None
        owner_id = result[0]
        return owner_id

    def owner_to_person(owner_id):
        curs.execute(f"SELECT person_id FROM owners WHERE owner_id = {owner_id}")
        result = curs.fetchone()
        if result is None:
            return None
        person_id = result[0]
        return person_id

    def owner_to_pet(owner_id):
        curs.execute(f"SELECT pet_id FROM pets WHERE owner_id = {owner_id}")
        result = curs.fetchone()
        if result is None:
            return None
        pet_id = result[0]
        return pet_id

    def person_to_vet(person_id):
        curs.execute(f"SELECT vet_id FROM vets WHERE person_id = {person_id}")
        result = curs.fetchone()
        if result is None:
            return None
        vet_id = result[0]
        return vet_id

    def owner_to_visit(owner_id):
        curs.execute(f"SELECT visit_id FROM visits WHERE owner_id = {owner_id} ")
        result = curs.fetchone()
        if result is None:
            return None
        visit_id = result[0]
        return visit_id

    def person_to_type(person_id):
        curs.execute(f"SELECT status FROM persons WHERE id = {person_id}")
        result = curs.fetchone()
        if result is None:
            return None
        vet_id = result[0]
        return vet_id
