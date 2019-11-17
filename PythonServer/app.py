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


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route("/publish/", methods=['POST'])
def publish():
    med_id = request.get_json()["id"]
    pill_id, dose = db.execute_query("SELECT pill_id, dose FROM med_times WHERE id='{}';".format(med_id))[0]
    payload = {
        "pill_id": pill_id,
        "dose": dose
    }
    publisher.publish(json.dumps(payload))
    pill_name, patient_id = db.execute_query("SELECT name, patient_id FROM pills WHERE id='{}';".format(pill_id))[0]
    patient_name, phone = db.execute_query("SELECT name, phone FROM patients WHERE id='{}';".format(patient_id))[0]
    msg = "Hi {0}! This is your reminder to take {1} pill(s) of {2}."\
        .format(patient_name.strip(), dose, pill_name.strip())
    # if phone:
    #     twilio.send_message(msg, phone)
    return "Success!"


if __name__ == '__main__':
   app.run("localhost", 8000)
