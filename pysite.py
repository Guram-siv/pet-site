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
    curs.execute('''INSERT INTO persons(name, lastname, phone, mail, address, created, status, password) 
    VALUES (%s, %s, %s, %s, %s, %s, %s,%s )''', (name, lastname, phone, mail, address, created, status, password))
    curs.execute("SELECT id FROM persons WHERE mail = %s and password = %s", (mail, password))
    result = curs.fetchone()
    global person_id
    person_id = result[0]
    connection.commit()
    print("registration completed succesfully") 
    
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

def register_pet(person_id):
  try:
    petname = input("Pet name: ")
    species = input("Type: ")
    breed = input("breed: ")
    gender = input("gender(M - male / F - female): ")
    byear = int(input("pet birth year: "))
    bmonth = int(input("Month: "))
    bday = int(input("Day: "))
    birthdate = date(byear, bmonth, bday)
    connection.commit()
    curs.execute("INSERT INTO owners(person_id) VALUES (%s)", (person_id, )) #inserting person id in owners to create owner id
    curs.execute("SELECT owner_id FROM owners WHERE person_id = %s", (person_id,))
    result = curs.fetchone()
    global owner_id          
    owner_id = result[0]     #getting owner_id from here and globalising it
    curs.execute('''INSERT INTO pets(species, breed, sex, name, birth_date, owner_id) 
    VALUES (%s, %s, %s, %s, %s, %s)''', (species, breed, gender, petname, birthdate, owner_id))
    curs.execute("SELECT pet_id FROM pets WHERE owner_id = %s", (owner_id, ))
    result = curs.fetchone()
    pet_id = result[0]       # getting pet id from here

    print(f"Pet registered succesfully! your pet was granted id of {pet_id}")
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

def log_in():
  mail = input("Please enter your email: ")
  curs.execute("SELECT password FROM persons WHERE mail = %s", ( mail, ))
  userpassword = curs.fetchone()
  if userpassword is not None:
    password = input("Please enter your password: ")
    if userpassword[0] == password:
        log = True
        curs.execute("SELECT status FROM persons WHERE mail = %s AND password = %s", (mail, password))
        global person_status
        person_s = curs.fetchone()
        person_status = person_s[0]
        curs.execute("SELECT id FROM persons WHERE mail = %s AND password = %s", (mail, password))
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
def stafflogin(person_id):
  print("Welcome dear staff member, your id is %s", (person_id, ))
  while True:
    print()
    action = input("what action should we do?\n1) List every owner, phone number and id\n2) List every vet, phone number and id\
\n3) List every pet name, type, breed and id\n4) Add my pet(makes me owner\staff memeber)\n5) List my pets(only for pet owners)\
\n0) log out\nq) quit the program \n: ")
    print()
    if action == "1":
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
      curs.execute("SELECT name, lastname, phone, id, status FROM persons WHERE status IN (4, 5)")
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
      register_pet(person_id)
      curs.execute("SELECT status FROM persons WHERE id = %s", (person_id, ))
      result = curs.fetchone()
      stat = result[0]
      if stat == "4":
        curs.execute("UPDATE persons SET status = 5 WHERE id = %s", (person_id, ))
        connection.commit()
      else:
        pass
    elif action == "5":
      curs.execute("SELECT owner_id FROM owners WHERE person_id = %s", (person_id, ))
      result = curs.fetchone()
      owner_id = result[0]
      if owner_id is not None:
        curs.execute("SELECT species, breed, sex, medical_condition, current_treatment, resent_vaccination, name, birth_date FROM pets WHERE owner_id = %s", (owner_id, ))
        pets = curs.fetchall()
        for pet in pets:
          species = pet[0]
          breed = pet[1]
          sex = pet[2]
          medical_condition = pet[3]
          current_treatment = pet[4]
          resent_vaccination = pet[5]
          name = pet[6]
          birth_date = pet[7]
          print(f"Species: {species}, Breed: {breed}, Gender: {sex}, Medical Condition: {medical_condition}, Current Treatment: {current_treatment}, Resent Vaccination: {resent_vaccination}, Name: {name}, Birth Date: {birth_date}")

      else:
        choise = input("it appears you dont have a pet, do you want to add one? (y/n)")
        if choise == "y":
          register_pet(person_id)
    elif action == "0":
      exit = False
      break
    elif action =="q":
      exit = True
      return exit
    else:
      print("the input was incorrect...")
      continue

def vetlogin(person_id):
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
      curs.execute("INSERT INTO visits(vet_id, pet_id, owner_id, diagnosis, date) VALUES (%s, %s, %s, %s, %s)", (vet_id, pets_id, owners_id, diagnosis, visitdate))
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
      return exit
    else:
      print("the input was incorrect...")
      continue


while True:
  action = input("login or register\n: ")
  if action == "login":
    log = log_in()
    if log == True:
      if person_status == 1:
        print("Welcome dear User, you registered as a pet owner, your id is %s", (person_id, ))
        welcome = input("Do you want to add pet now? (y / n): ")
        if welcome == "y":
          register_pet(person_id)
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
            if owner_id is not None:
              curs.execute("SELECT species, breed, sex, medical_condition, current_treatment, resent_vaccination, name, birth_date FROM pets WHERE owner_id = %s", (owner_id, ))
              pets = curs.fetchall()
              for pet in pets:
                species = pet[0]
                breed = pet[1]
                sex = pet[2]
                medical_condition = pet[3]
                current_treatment = pet[4]
                resent_vaccination = pet[5]
                pet_name = pet[6]
                birth_date = pet[7]
                print(f"Species: {species}, Breed: {breed}, Gender: {sex}, Medical Condition: {medical_condition}, Current Treatment: {current_treatment}, Resent Vaccination: {resent_vaccination}, Name: {pet_name}, Birth Date: {birth_date}")
            else:
              print("you dont have pets currently")
          elif action == "2":
            curs.execute("SELECT * FROM visits WHERE person_id = %s;", (person_id, )) 
            result = curs.fetchone()
            owner_id = result[0]
            for visit in visits:
              visit_id = visit[0]
              vet_id = visit[1]
              pet_id = visit[2]
              owner_id = visit[3]
              diagnosis = visit[4]
              treatment = visit[5]
              date = visit[6]
              print(f"Visit ID: {visit_id}, Vet ID: {vet_id}, Pet ID: {pet_id}, Owner ID: {owner_id}, Diagnosis: {diagnosis}, Treatment: {treatment}, Date: {date}")

            else:
              print("you dont have pets, hence you got no visits")
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
            register_pet(person_id)
          elif choise == "n":
            pass
          else:
            print("something went wrong with input! logging out")
            continue
        else:
          stafflogin(person_id)
        
      elif person_status == 4 or person_status == 5:
        if person_status == 5:
          choise = input("It appears you have a pet... do you want to add it now?(y/n)\n:")
          if choise == "y":
            register_pet(person_id)
          elif choise == "n":
            pass
          else:
            print("something went wrong with input! logging out")
            continue
        print("Hello Dear vet, your id is %s", (person_id, ))
        curs.execute("SELECT vet_id FROM vets WHERE person_id = %s;", (person_id, ))
        result = curs.fetchone()
        vet_id = result[0]
        vetlogin(person_status, person_id)
      elif person_status == 6 or person_status == 7:
        print("Hello Dear staff/vet")
        if person_status == 7:
          choise = input("It appears you have a pet... do you want to add it now?(y/n)\n:")
          if choise == "y":
            register_pet(person_id)
          elif choise == "n":
            pass
        while True:
          choose = input("do you want to enter as staff or vet?\n1)Staff member\n2)Vet\n: ")
          if choose == "1":
            print("You are in staff sub menu")
            stafflogin(person_id)
          if choose == "2":
            print("You are in vet sub menu")
            vetlogin(person_id)





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

    if choise == 2 or choise == 3:
      person_id = person_id
      curs.execute("INSERT INTO help_centre(person_id, status) VALUES (%s, %s)", (person_id, choise))
      
    elif choise == 4 or choise == 5:
      person_id = person_id
      curs.execute("INSERT INTO vets(person_id) VALUES(%s)", (person_id,))

    elif choise == 6 or choise == 7:
      person_id = person_id
      curs.execute("INSERT INTO help_centre(person_id, status) VALUES (%s, %s)", (person_id, choise))
      curs.execute("INSERT INTO vets(person_id) VALUES(%s)", (person_id,))
    
    if choise == 1 or choise == 3 or choise == 5 or choise == 7:
      haspet = input("Do you want to register a pet?\n(y - yes / n - no): ")
      if haspet.lower() == "y" or haspet.lower() == "yes":
        person_id = person_id
        register_pet(person_id)
        log_in()
      elif haspet.lower() == "n" or haspet.lower() == "no":
        log = input("do you want to return to main menu? (y - yes / n - exit): ")
        if log == "n":
          break
        else:
          continue
      else:
        continue
      #last = input("registration has been succesfull!")
curs.close()
connection.close()