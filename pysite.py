import psycopg2
from config import config
from datetime import date, datetime

connection = None
params = config()
connection = psycopg2.connect(**params)
curs = connection.cursor()


def register_person(status):
  try:
    name = input("Name: ")
    password= input("password: ")
    lastname = input("Lastname: ")
    phone = int(input("Phone number: "))   
    mail = input("Mail: ")
    address = input("Address: ")
    created = date.today()
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

def register_pet(owner_id):
  try:
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
    curs.execute('''INSERT INTO pets(species, breed, sex, medical_condition, current_treatment, name, birth_date, owner_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (species, breed, gender, medical_condition, current_treatment, petname, birthdate, owner_id))

    connection.commit()
    print("Pet registered succesfully!")
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

def log_in(mail, password):
  curs.execute("SELECT owners.password FROM owners JOIN persons ON owners.person_id = persons.id WHERE persons.mail = %s", ( mail, ))
  userpassword = curs.fetchone()
  if userpassword is not None:
    if userpassword[0] == password:
        log = True
        curs.execute("SELECT persons.status FROM persons JOIN owners ON persons.id = owners.person_id WHERE persons.mail = %s AND owners.password = %s", (mail, password))
        global person_status
        person_s = curs.fetchone()
        person_status = person_s[0]
        curs.execute("SELECT persons.id FROM persons JOIN owners ON persons.id = owners.person_id WHERE persons.mail = %s AND owners.password = %s", (mail, password))
        global person_id
        person = curs.fetchone()
        person_id = person[0]
        curs.close()
    else:
      print("Incorrect password.")
      log = False
      return log
  else:
    print("Email not found.")
    log = False
    return log
  

while True:
  action = input("login or register\n: ")
  if action == "login":
    mail = input("Please enter your email: ")
    password = input("Please enter your password: ")
    log = log_in(mail, password)
    if log == True:
      if person_status == 1:
        welcome = input("Welcome dear User,\n Do you want to add pet now? (y / n): ")
        if welcome == "y":
          curs.execute("INSERT INTO owners(person_id) VALUES (%s);", (person_id, ))
          curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
          result = curs.fetchone()
          owner_id = result[0]
          register_pet(owner_id)
        action = input("What should we do?\n 1) my pets\n2) my visits\n 0) log out \nq) Exit program \n: ")
        if action == "1":
          curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
          result = curs.fetchone()
          owner_id = result[0]
          curs.execute("SELECT * FROM pets WHERE owner_id = %s", (owner_id, ))
          petname = curs.fetchall()
          for pet in petname:
            for i in pet:
              print(i, end=' ')
            print()
        elif action == "2":
          curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
          result = curs.fetchone()
          owner_id = result[0]
          curs.execute("SELECT * FROM visits WHERE owner_id = %s", (owner_id, ))
          visits = curs.fetchall()
          for visit in visits:
            for i in visit:
              print(i, end=' ')
            print()
        elif action == "0":
          continue
        elif action =="q":
          break
        else:
          print("the input was incorrect...")
          continue
      elif person_status == 2:


        



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
    

    register_person(choise)
    
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
      print("choise input was incorrect")
      continue
    if choise == 1 or 3 or 5 or 7:
      haspet = input("Do you want to register a pet?\n(y - yes / n - no): ")
      if haspet == "y" or "yes" or "Yes" or "YES":
        owner_id = owner_id
        register_pet(owner_id)
      elif haspet == "n" or "no" or "No" or "NO":
        log = input("do you want to log in? (y - yes / n - no): ")
      
      else:
        continue
      #last = input("registration has been succesfull!")
         
connection.close()