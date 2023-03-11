import psycopg2
from config import config

connection = None
params = config()
connection = psycopg2.connect(**params)
curs = connection.cursor()

def connect():
  try:
    print("Connecting...\nPostgresSQL database version: ")
    curs.execute('SELECT version()')
    db_version = curs.fetchone()
    print(db_version)
    curs.close()
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)
#  finally:
#   if connection is not None:
#      connection.close()
#      print("Connection terminated...")
#if __name__ =="__main__":
  #connect()

def getData():
  try:
    table = input("table name: ")
    curs.execute(f'SELECT * FROM {table}')
    rows = curs.fetchall()
    for r in rows:
      print(r)
    curs.close()
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)


def insertPersons(status):
  try:
    name = input("name: ")
    lastname = input("lastname: ")
    phone = input("phone number: ")
    mail = input("mail: ")
    address = input("address ")
    curs.execute(f'''INSERT INTO persons(name, lastname, phone, mail, address, status) 
    VALUES ({name}, {lastname}, {phone}, {mail}, {address}, {status}) ''')
    connection.commit()
    print("Data inserted successfully")
    curs.close()
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)

#under construction

def insertpet(owner_id):
  try:
    species = input("species: ")
    breed = input("breed: ")
    gender = input("gender(F- for female, M- for male): ")
    medical_condition = input("medical_condition: ")
    current_treatment = input("current_treatment: ")
    name = input("pet name: ")
    birthdate = input("birth date: ")
    curs.execute(f'''INSERT INTO pets(species, breed, gender, medical_condition, current_treatment, name, birthdate, owner_id) 
    VALUES ({species}, {breed}, {gender}, {medical_condition}, {current_treatment}, {name}, {birthdate}, {owner_id}) ''')
    connection.commit()
    print("Data inserted successfully")
    curs.close()
  except(Exception, psycopg2.DatabaseError) as error:
    print(error)


def insertprototype(conn, table_name, values):
    curs = conn.cursor()
    curs.execute(f"SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '{table_name}'")
    num_cols = curs.fetchone()[0]
    placeholders = ",".join(["%s"] * num_cols)
    curs.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
    col_names = [col[0] for col in curs.fetchall()]
    sql = f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})"
    curs.execute(sql, values)
    conn.commit()

#insertprototype(connection, "statuses", (8, "Test"))
connection.close()
curs.close()