from app import config
from db_connection import DBConnection
import random

IMPORT_UUID_GENERATOR = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'

CREATE_PATIENT_TABLE = "CREATE TABLE patients (" \
                       "id uuid DEFAULT uuid_generate_v4 (), " \
                       "name CHAR(50) NOT NULL, " \
                       "phone CHAR(15), " \
                       "PRIMARY KEY (id) );"

CREATE_PILL_TABLE = "CREATE TABLE pills (" \
                    "id uuid DEFAULT uuid_generate_v4 (), " \
                    "patient_id uuid NOT NULL, " \
                    "name CHAR(50) NOT NULL, " \
                    "quantity INTEGER NOT NULL," \
                    "PRIMARY KEY (id) );"

CREATE_MEDTIMES_TABLE = "CREATE TABLE med_times (" \
                       "id uuid DEFAULT uuid_generate_v4 (), " \
                       "pill_id uuid NOT NULL, " \
                       "day INTEGER NOT NULL," \
                       "time TIME WITHOUT TIME ZONE NOT NULL, " \
                       "dose INTEGER NOT NULL," \
                       "PRIMARY KEY (id) );"

INSERT_PILL = "INSERT INTO pills (patient_id, name, quantity)" \
                  "VALUES ('{0}', '{1}', 20);"
PILL_NAMES = ["Vitamin B", "Iron", "Calcium", "Ego", "Gravel", "Xanax"]

INSERT_MEDTIME = "INSERT INTO med_times (pill_id, day, time, dose)" \
                  "VALUES ('{0}', {1}, '12:00:00', {2});"

db = DBConnection(config("postgresql"))

db.execute(IMPORT_UUID_GENERATOR)
db.execute(CREATE_PATIENT_TABLE)
db.execute(CREATE_PILL_TABLE)
db.execute(CREATE_MEDTIMES_TABLE)


db.execute("INSERT INTO patients (name, phone) VALUES ('Jane Smith', '+15199659801');")
patient_id, = db.execute_query("SELECT id FROM patients;")[0]
for pill in PILL_NAMES:
    db.execute(INSERT_PILL.format(patient_id, pill))
pill_id, = db.execute_query("SELECT id FROM pills;")[0]
for i in range(4):
    db.execute(INSERT_MEDTIME.format(pill_id, random.randint(1, 7), random.randint(1, 2)))

db.close()
