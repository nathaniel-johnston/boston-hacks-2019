from app import config
from db_connection import DBConnection
import random


CREATE_PATIENT_TABLE = "CREATE TABLE patients (" \
                       "id SERIAL PRIMARY KEY, " \
                       "name CHAR(50) NOT NULL, " \
                       "phone CHAR(15) );"

CREATE_PILL_TABLE = "CREATE TABLE pills (" \
                    "id SERIAL PRIMARY KEY, " \
                    "patient_id INTEGER NOT NULL, " \
                    "name CHAR(50) NOT NULL, " \
                    "quantity INTEGER NOT NULL, " \
                    "time TIME WITHOUT TIME ZONE NOT NULL, " \
                    "dose INTEGER NOT NULL );"

INSERT_PILL = "INSERT INTO pills (patient_id, name, quantity, time, dose)" \
                  "VALUES ('{0}', '{1}', 20, '{2}:00:00', {3});"
PILL_NAMES = ["Vitamin B", "Iron", "Calcium", "Ego", "Gravel", "Xanax"]

db = DBConnection(config("postgresql"))

db.execute(CREATE_PATIENT_TABLE)
db.execute(CREATE_PILL_TABLE)


db.execute("INSERT INTO patients (name, phone) VALUES ('Jane Smith', '+15199659801');")
patient_id, = db.execute_query("SELECT id FROM patients;")[0]
for pill in PILL_NAMES:
    db.execute(INSERT_PILL.format(patient_id, pill, random.randint(0, 24), random.randint(1, 3)))

db.close()
