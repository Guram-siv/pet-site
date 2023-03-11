import psycopg2
from config import config

connection = None
params = config()
connection = psycopg2.connect(**params)
curs = connection.cursor()


def register_person(name, lastname, phone, mail, address, status):
  try:
    curs.execute(f'''INSERT INTO persons(name, lastname, phone, mail, address, status) 
    VALUES ({name}, {lastname}, {phone}, {mail}, {address}, {status}) ''')
    connection.commit()
    curs.close()
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

def register_pet(species, breed, gender, medical_condition, current_treatment, name, birthdate, owner_id):
  try:
    curs.execute(f'''INSERT INTO pets(species, breed, gender, medical_condition, current_treatment, name, birthdate, owner_id) 
    VALUES ({species}, {breed}, {gender}, {medical_condition}, {current_treatment}, {name}, {birthdate}, {owner_id}) ''')
    connection.commit()
    curs.close()
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)


connection.close()