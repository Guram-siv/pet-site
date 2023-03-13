import psycopg2
from config import config
from datetime import date, datetime

connection = None
params = config()
connection = psycopg2.connect(**params)
curs = connection.cursor()


def register_person(name, lastname, phone, mail, address, created, status):
  try:
    curs.execute('''INSERT INTO persons(name, lastname, phone, mail, address, created, status) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)''', (name, lastname, phone, mail, address, created, status))
    curs.execute("SELECT id FROM persons WHERE name = %s AND mail = %s", (name, mail))
    result = curs.fetchone()
    global person_id
    person_id = result[0]
    curs.execute("INSERT INTO owners(person_id, password) VALUES (%s, %s)", (person_id, password))
    curs.execute("SELECT owner_id FROM owners WHERE person_id = %s", (person_id,))
    result = curs.fetchone()
    global owner_id
    owner_id = result[0]
    connection.commit()
    print("registration completed succesfully") #####STOPPED HERE
    
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

def register_pet(species, breed, gender, medical_condition, current_treatment, name, birthdate, owner_id):
  try:
    curs.execute('''INSERT INTO pets(species, breed, sex, medical_condition, current_treatment, name, birth_date, owner_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (species, breed, gender, medical_condition, current_treatment, name, birthdate, owner_id))

    connection.commit()
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

while True:
  action = input("login or register\n: ")
  if action == "login":
    mail = input("Please enter your email: ")
    curs.execute("SELECT owners.password FROM owners JOIN persons ON owners.person_id = persons.id WHERE persons.mail = %s", ( mail, ))
    userpassword = curs.fetchone()

    if userpassword is not None:
        password = input("Please enter your password: ")
        if userpassword[0] == password:
            while True:
              action = input("Login successful!\nif you want to exit type ( q ): ")
              if action == "q":
                break
        else:
            print("Incorrect password.")
    else:
        print("Email not found.")

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
7) Pet owner, staff member and vet\n\: "))
    except:
      print("Please enter the given numbers...")
    name = input("Name: ")
    password= input("password: ")
    lastname = input("Lastname: ")
    try:
      phone = int(input("Phone number: "))
    except:
      print("phone number should be phone number... exiting program")
      break
    mail = input("Mail: ")
    address = input("Address: ")
    created = date.today()

    register_person(name, lastname, phone, mail, address, created, choise)
    
    connection.commit()
    if choise == 2 or 3:
      person_id = person_id
      curs.execute("INSERT INTO help_centre(person_id, status) VALUES (%s, %s)", (person_id, choise))
      curs.close()
    elif choise == 4 or 5:
      person_id = person_id
      curs.execute("INSERT INTO vets(person_id) VALUES(%s)", (person_id,))
      curs.close()
    elif choise == 6 or 7:
      person_id = person_id
      curs.execute("INSERT INTO help_centre(person_id, status) VALUES (%s, %s)", (person_id, choise))
      curs.execute("INSERT INTO vets(person_id) VALUES(%s)", (person_id,))
      curs.close()
    else:
      continue
    if choise == 1 or 3 or 5 or 7:
      haspet = input("Do you want to register a pet?\n(y - yes / n - no): ")
      if haspet == "y" or "yes" or "Yes" or "YES":
        species = input("Species: ")
        breed = input("breed: ")
        gender = input("gender(M - male / F - female): ")
        medical_condition = input("Medical condition (if none type healthy): ")
        current_treatment = input("Current treatment(if none type healthy):")
        petname = input("Pet name: ")
        byear = int(input("pet birth year: "))
        bmonth = int(input("Month: "))
        bday = int(input("Day: "))
        birthdate = date(byear, bmonth, bday)
        owner_id = owner_id
        register_pet(species, breed, gender, medical_condition, current_treatment, petname, birthdate, owner_id)
      
      else:
        continue
      #last = input("registration has been succesfull!")
         
connection.close()