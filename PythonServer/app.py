from flask import Flask, request
from configparser import ConfigParser
from mqtt_connection import MQTTConnection
from twilio_connection import TwilioConnection
from db_connection import DBConnection
import json


def config(section, filename='config.ini'):
    parser = ConfigParser()
    parser.read(filename)

    values = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            values[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return values


publisher = MQTTConnection(config("mqtt"))
twilio = TwilioConnection(config("twilio"))
db = DBConnection(config("postgresql"))

app = Flask(__name__)


@app.route("/pills/<patient_id>", methods=['GET'])
def pills(patient_id):
    db_pill = db.execute_query("SELECT id, name, quantity, time, dose FROM pills WHERE patient_id='{}';"
                               .format(patient_id))
    pills_arr = []
    for pill_id, name, quantity, time, dose in db_pill:
        pills_arr.append({
            "pill_id": pill_id,
            "name": name.strip(),
            "quantity": quantity,
            "time": str(time),
            "dose": dose
        })
    return json.dumps({"pills": pills_arr})


@app.route("/new/pill", methods=['POST'])
def new_pill():
    data = request.get_json()
    patient_id = data["patient_id"]
    name = data["name"]
    quantity = data["quantity"]
    time = data["time"]
    dose = data["dose"]

    pill_id = db.execute("INSERT INTO pills (id, patient_id, name, quantity, time, dose) "
                         "VALUES (DEFAULT, {0}, '{1}', {2}, '{3}', {4}) RETURNING id;"
                         .format(patient_id, name, quantity, time, dose), returning=True)
    return json.dumps({"pill_id": pill_id})


@app.route("/pill/<pill_id>", methods=['PUT'])
def update_pill(pill_id):
    data = request.get_json()
    patient_id = data["patient_id"]
    name = data["name"]
    quantity = data["quantity"]
    time = data["time"]
    dose = data["dose"]

    db.execute("UPDATE pills SET "
               "patient_id={0}, name='{1}', quantity={2}, time='{3}', dose={4} "
               "WHERE id={5};"
               .format(patient_id, name, quantity, time, dose, pill_id))
    return ""


@app.route("/dispense", methods=['POST'])
def dispense():
    pill_id = request.get_json()["id"]
    dose, = db.execute_query("SELECT dose FROM pills WHERE id={};".format(pill_id))[0]
    payload = {
        "pillId": pill_id-1,
        "numPills": dose
    }
    publisher.publish(payload)
    return ""


@app.route("/remind", methods=['POST'])
def remind():
    pill_id = request.get_json()["id"]
    pill_name, patient_id, dose = db.execute_query("SELECT name, patient_id, dose FROM pills WHERE id='{}';"
                                                   .format(pill_id))[0]
    patient_name, phone = db.execute_query("SELECT name, phone FROM patients WHERE id='{}';".format(patient_id))[0]
    msg = "Hi {0}! This is your reminder to take {1} pill(s) of {2}."\
        .format(patient_name.strip(), dose, pill_name.strip())
    if phone:
        twilio.send_message(msg, phone)
    return ""


if __name__ == '__main__':
   app.run("localhost", 8000)
