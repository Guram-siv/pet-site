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
    lastname = input("Lastname: ")
    phone = int(input("Phone number: "))   
    mail = input("Mail: ")
    password= input("password: ")
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
    petname = input("Pet name: ")
    species = input("Type: ")
    breed = input("breed: ")
    gender = input("gender(M - male / F - female): ")
    byear = int(input("pet birth year: "))
    bmonth = int(input("Month: "))
    bday = int(input("Day: "))
    birthdate = date(byear, bmonth, bday)
    curs.execute('''INSERT INTO pets(species, breed, sex, name, birth_date, owner_id) 
    VALUES (%s, %s, %s, %s, %s, %s)''', (species, breed, gender, petname, birthdate, owner_id))
    connection.commit()
    curs.execute("SELECT pet_id FROM pets WHERE owner_id = %s", (owner_id))
    result = curs.fetchone()
    pet_id = result[0]
    print("Pet registered succesfully! your pet has this %s id", (pet_id))
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

def log_in():
  mail = input("Please enter your email: ")
  curs.execute("SELECT owners.password FROM owners JOIN persons ON owners.person_id = persons.id WHERE persons.mail = %s", ( mail, ))
  userpassword = curs.fetchone()
  if userpassword is not None:
    password = input("Please enter your password: ")
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
        return log
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
    log = log_in()
    if log == True:
      if person_status == 1:
        print("Welcome dear User, you registered as a pet owner, your id is %s", (person_id, ))
        welcome = input("Do you want to add pet now? (y / n): ")
        if welcome == "y":
          curs.execute("INSERT INTO owners(person_id) VALUES (%s);", (person_id, ))
          curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
          result = curs.fetchone()
          owner_id = result[0]
          register_pet(owner_id)
        elif welcome == "n":
          pass
        else:
          print("something went wrong with input! logging out")
          continue
        while True:
          action = input("\n\n\nWhat should we do?\n1) my pets\n2) my visits\n0) log out \nq) Exit program \n: ")
          if action == "1":
            curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
            result = curs.fetchone()
            owner_id = result[0]
            curs.execute("SELECT species, breed, sex, medical_condition, current_treatment, resent_vaccination, name, birth_date FROM pets WHERE owner_id = %s", (owner_id, ))
            petname = curs.fetchall()
            for pet in petname:
              for i in pet:
                print(i, end=', ')
              print()
          elif action == "2":
            curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
            result = curs.fetchone()
            owner_id = result[0]
            curs.execute("SELECT * FROM visits WHERE owner_id = %s", (owner_id, ))
            visits = curs.fetchall()
            for visit in visits:
              for i in visit:
                print(i, end=', ')
              print()
          elif action == "0":
            exit = False
            break
          elif action =="q":
            exit = True
            break
          else:
            print("the input was incorrect...")
            continue
        if exit == True:
          break
        else:
          continue
      elif person_status == 2 or person_status == 3:
        if person_status == 3:
          choise = input("It appears you have a pet... do you want to add it now?(y/n)\n:")
          if choise == "y":
            curs.execute("INSERT INTO owners(person_id) VALUES (%s);", (person_id, ))
            curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
            result = curs.fetchone()
            owner_id = result[0]
            register_pet(owner_id)
          elif choise == "n":
            pass
          else:
            print("something went wrong with input! logging out")
            continue
        print("Welcome dear staff member, your id is %s", (person_id, ))
        while True:
            action = input("what action should we do?\n1) List every owner, phone number and id\n2) List every vet, phone number and id\n3) List every pet name, type, breed and id\n4) Add my pet(makes me owner\staff memeber)\n5) List my pets(only for pet owners)\n0) log out\nq) quit the program ")
            if action == "1":
              curs.execute("SELECT name, lastname, phone, id FROM persons WHERE status = 1")
              persons = curs.fetchall()
              for person in persons:
                for i in person:
                  print(i, end=', ')
                print()
            elif action == "2":
              curs.execute("SELECT name, lastname, phone, id, status FROM persons WHERE status IN (4, 5)")
              persons = curs.fetchall()
              for person in persons:
                for i in person:
                  if i == 5:
                      print("is vet", end=', ')
                  else:
                      print(i, end=', ')
                print()
            elif action == "3":
              curs.execute("SELECT pets.name, pets.type, pets.breed, pets.id, persons.name, pets.pet_id|| ' ' ||\
 persons.lastname as owner_name FROM pets JOIN persons ON pets.owner_id = persons.id")
              pets = curs.fetchall()
              for pet in pets:
                for i in pet:
                  print(i, end=', ')
                print()
            elif action == "4":
              register_pet(person_id)
              curs.execute("SELECT status FROM persons WHERE id =%s", (person_id))
              result = curs.fetchone()
              stat = result[0]
              if stat == "4":
                curs.execute("UPDATE persons SET status = 5 WHERE id = %s", (person_id))
                connection.commit()
              else:
                pass
            elif action == "5":
              curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
              result = curs.fetchone()
              owner_id = result[0]
              curs.execute("SELECT species, breed, sex, medical_condition, current_treatment, resent_vaccination, name, birth_date FROM pets WHERE owner_id = %s", (owner_id, ))
              petname = curs.fetchall()
              for pet in petname:
                for i in pet:
                  print(i, end=', ')
                print()
            elif action == "0":
              exit = False
              break
            elif action =="q":
              exit = True
              break
            else:
              print("the input was incorrect...")
              continue
      elif person_status == 4 or person_status == 5:
        if person_status == 5:
          choise = input("It appears you have a pet... do you want to add it now?(y/n)\n:")
          if choise == "y":
            curs.execute("INSERT INTO owners(person_id) VALUES (%s);", (person_id, ))
            curs.execute("SELECT owner_id FROM owners WHERE person_id = %s;", (person_id, ))
            result = curs.fetchone()
            owner_id = result[0]
            register_pet(owner_id)
          elif choise == "n":
            pass
          else:
            print("something went wrong with input! logging out")
            continue
        print("Hello Dear vet, your id is %s", (person_id, ))
        curs.execute("SELECT vet_id FROM vets WHERE person_id = %s;", (person_id, ))
        result = curs.fetchone()
        vet_id = result[0]
        while True:
          action = input("What action should we perform?\n1) add a new entry in visits\n2) List my med history\n3) add my speciality \n4) add my pet(makes me owner/vet)\n0) log out\nq) exit program")
          if action == "1":
            owners_id = input("Please input owner id: ")
            pets_id = input("Please input pet id: ")
            diagnosis = input("What was the diagnosis?: ")
            vaccination = input("Was pet vaccinated? (y/n): ")
            visitdate = date.today()
            if vaccination == "y":
              vacdate = date.today()
              curs.execute("INSERT INTO pets(resent_vaccination) VALUES (%s) WHERE pet_id = %s", (vacdate, pets_id))
              connection.commit()
            else:
              pass
            treat = input("Does pet have current treatment? (y/n):")
            if treat == "y":
              treatment = input("explain the treatment: ")
              curs.execute("INSERT INTO pets(current_treatment) VALUES (%s) WHERE pet_id = %s", (treatment, pets_id))
              connection.commit()
            else:
              pass
            curs.execute("INSERT INTO visits(vet_id, pet_id, owner_id, diagnosis, date) VALUES (%s, %s, %s, %s, %s)", (vet_id, pets_id, owner_id, diagnosis, visitdate))
            connection.commit()
          elif action == "2":
            curs.execute("SELECT * FROM visits WHERE vet_id = %s", (vet_id, ))
            visits = curs.fetchall()
            for visit in visits:
              for i in visit:
                print(i, end=', ')
              print()
          elif action == "3":
            while True:
              choose = input("1) add my speciality\n2) list specialities\n0) Go to main menu")
              if choose == "1":
                speciality = "My speciality: "
                speciality.lower()
                speciality.capitalize()
                curs.execute("SELECT specialty FROM specialities")
                results = curs.fetchall()
                specialities_list = [result[0] for result in results]
                if speciality in specialities_list:
                  curs.execute("SELECT spec_id FROM specialities WHERE specialty = %s", (speciality))
                  result = curs.fetchone()
                  spec_id = result[0]
                  curs.execute("INSERT INTO spec_combo(vet_id, spec_id) VALUES (%s, %s)", (vet_id, spec_id))
                  connection.commit()
                else:
                  print(f"There is no {speciality} speciality in our database, either contact the staff or try again")
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
            register_pet(person_id)
            curs.execute("SELECT status FROM persons WHERE id =%s", (person_id))
            result = curs.fetchone()
            stat = result[0]
            if stat == "4":
              curs.execute("UPDATE persons SET status = 5 WHERE id = %s", (person_id))
              connection.commit()
            else:
              pass
          elif action == "0":
            exit = False
            break
          elif action =="q":
            exit = True
            break
          else:
            print("the input was incorrect...")
            continue




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
    

    register_person(choise)
    
    connection.commit()
    if choise == 2 or choise == 3:
      person_id = person_id
      curs.execute("INSERT INTO help_centre(person_id, status) VALUES (%s, %s)", (person_id, choise))
      curs.close()
    elif choise == 4 or choise == 5:
      person_id = person_id
      curs.execute("INSERT INTO vets(person_id) VALUES(%s)", (person_id,))
      curs.close()
    elif choise == 6 or choise == 7:
      person_id = person_id
      curs.execute("INSERT INTO help_centre(person_id, status) VALUES (%s, %s)", (person_id, choise))
      curs.execute("INSERT INTO vets(person_id) VALUES(%s)", (person_id,))
      curs.close()
    
    if choise == 1 or choise == 3 or choise == 5 or choise == 7:
      haspet = input("Do you want to register a pet?\n(y - yes / n - no): ")
      if haspet.lower() == "y" or haspet.lower() == "yes":
        owner_id = owner_id
        register_pet(owner_id)
      elif haspet.lower() == "n" or haspet.lower() == "no":
        log = input("do you want to return to main menu? (y - yes / n - exit): ")
        if log == "n":
          break
        else:
          continue
      else:
        continue
      #last = input("registration has been succesfull!")
